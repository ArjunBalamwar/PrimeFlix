from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import PostForm1, PostForm2, PostForm3, PostForm4, PostForm, Search, PostDeleteForm
from django.core.mail import send_mail
from django.contrib import messages
from .models import Post, WatchLater, Like
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (ListView, DetailView, CreateView,
                                  UpdateView, DeleteView
)
from rest_framework.response import Response
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.metrics.pairwise import linear_kernel
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import nltk
import numpy as np
from nltk.corpus import stopwords
import re
import string as strg
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from collections import Counter
import joblib

def sentence_engineering(string):
    ps = PorterStemmer()
    reverse = ["not", "isn't", "wasn't", "won't", "don't", "n't", "can't", "couldn't", "wouldn't"]
    custom_stop = [word for word in stopwords.words('english') if word not in reverse]  
    regex = re.compile('[%s]' % re.escape(strg.punctuation))
    string = regex.sub('', string).lower().split()
    string = [ps.stem(word) for word in string if word not in custom_stop]
    return ' '.join(string)

def sentence_engineering(string):
    wl = WordNetLemmatizer()
    custom_stop = [word for word in stopwords.words('english') if word not in reverse]  
#     custom_stop = []
    regex = re.compile('[%s]' % re.escape(strg.punctuation))
    string = regex.sub('', string).lower().split()
    string = [wl.lemmatize(word, pos='v') for word in sentence_engineering_(string)]
    return ' '.join(string)

def sentence_engineering_(text):
    tokens_tag = nltk.pos_tag(text)
    patterns= """NP:{<NN.?>*<VB.?>*<WP.?>*<PRP.?>*<MD.?>*<RB.?>*<WRB.?>*<JJ.?>*<CC>?}"""
    chunker = nltk.RegexpParser(patterns)
    output = chunker.parse(tokens_tag)
    chunked_list = []
    for elem in output:
        if isinstance(elem, nltk.Tree):
            chunked = []
            for (text, tag) in elem:
                if text not in ["are", 'am']:
                    chunked += text.split()
            chunked_list+= chunked
    return chunked_list

def sent_eng(string):
    return ' '.join([''.join(i.split(' ')) for i in string.split(',')])  
    
def Search_bar(posts, title):
    df_temp = pd.read_csv("df_clean.csv")
    string = sentence_engineering(title)
    string = sent_eng(string)
    tfidf = joblib.load("vectorizer.pkl")

    cos = linear_kernel(tfidf.transform([string]).toarray(), tfidf.transform(df_temp["name"]+" "+df_temp["name"]+" "+df_temp["cast"]+" "+df_temp["country"]+" "+df_temp["genres"]).toarray())
    sim_scores = list(enumerate(cos[0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[0:11]
    movie_indices = [i[0] for i in sim_scores]
    print(movie_indices)
    post_list = []
    for i in movie_indices:
        post_list.append(posts[i])
    return post_list

def search(posts, name):
    strings = name.lower().split()
    category_posts = []
    for post in posts:
        for string in strings:
            data = post.name+" "+post.name+" "+ post.cast +" "+ post.country+" "+ post.genres+" "+ post.type
            if string in data.lower().split():
                category_posts.append(post)
    
    result = [item for items, c in Counter(category_posts).most_common() for item in [items] * c]
    
    res = []
    for item in result:
        flag = True
        for r in res:
            if item.name == r.name:
                flag = False
                break
        if flag:
            res.append(item)
    return res



def mainHome(request):
    return render(request, 'blog/index.html',)


def home(request):
    posts = Post.objects.all().order_by("-likes")
    if request.method== 'POST':
        form = Search(request.POST)
        if form.is_valid():
            cats = form.cleaned_data.get('search')
            return redirect("home-search", cats)
    else:
        form = Search()
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    context={
        'page': page,
        'post_list': post_list,
        'search_form': form,
        'text': "No Movies And Shows Available",
    }
    return render(request, 'blog/index.html', context)

def home_search(request, cats):
    posts = Post.objects.all().order_by("-likes")
    if request.method== 'POST':
        form = Search(request.POST)
        if form.is_valid():
            cats = form.cleaned_data.get('search')
            return redirect("home-search", cats)
    else:
        form = Search()
    posts  = search(posts, cats)
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    context={
        'page': page,
        'post_list': post_list,
        'search_form': form,
        'text': "No Movies And Shows Found",
    }
    return render(request, 'blog/index.html', context)



def about(request):
    df = pd.read_csv("df_pure.csv")
    for index in range(len(df)):
        entry = df.loc[index]
        model = Post()
        model.name = entry['name']
        model.type = entry['type']
        model.content = entry['content']
        model.director = entry['director']
        model.cast = entry['cast']
        model.country = entry['country']
        model.genres = entry['genres']
        model.duration = entry['duration']
        model.release_date = entry['release_date']
        model.likes = 10
        model.rating = entry['rating']
        model.save()
        
    return render(request, 'blog/about.html')

def vectorize(df_temp, descriptions, titles):
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(descriptions)
    cosine_sim1 = linear_kernel(tfidf_matrix, tfidf_matrix)

    indices = pd.Series(df_temp.index, index = titles)
    return cosine_sim1, indices, tfidf

@login_required
def PostCreateView(request):
    df = pd.read_csv("df_pure.csv")
    df_temp = pd.read_csv('df_clean.csv')
    if request.user.is_superuser:
        if request.method== 'POST':
            form=PostForm(request.POST)
            if form.is_valid():
                post = Post()
                post.name = form.cleaned_data["name"]
                post.type = form.cleaned_data["type"]
                post.content = form.cleaned_data["content"]
                post.director = form.cleaned_data["director"]
                post.cast = form.cleaned_data["cast"]
                post.country = form.cleaned_data["country"]
                post.genres = ', '.join(form.cleaned_data["genres"])
                post.duration = form.cleaned_data["duration"]
                post.release_date = form.cleaned_data["release_date"]
                post.likes = form.cleaned_data["likes"]
                post.rating = ', '.join(form.cleaned_data["rating"])
                data_map = {'name': [post.name], 'type': [post.type], 'content': [post.content], 'director': [post.director], 'cast': [post.cast], 'country': [post.country], 'genres': [post.genres], 'duration': [post.duration], 'release_date': [post.release_date], 'likes': [post.likes], 'rating': [post.rating]}
                df = df.append(pd.DataFrame(data_map), ignore_index=True)
                data_map['content'][0] = sentence_engineering(data_map['content'][0])
                data_map['name'][0] = sent_eng(data_map['name'][0])
                data_map['director'][0] = sent_eng(data_map['director'][0])
                data_map['cast'][0] = sent_eng(data_map['cast'][0])
                df_temp = df_temp.append(pd.DataFrame(data_map), ignore_index=True)
                cosine_sim, indices, tfidf = vectorize(df_temp, df_temp["name"]+" "+df_temp["cast"]+" "+df_temp["country"]+" "+df_temp["genres"], df["name"])
                joblib.dump(tfidf, "vectorizer.pkl")
                post.save()
                df.to_csv('df_pure.csv')
                print(pd.read_csv("df_pure.csv"))
                df_temp.to_csv('df_clean.csv')
                messages.success(request, f'New entry added')
                return redirect("blog-home")
            else:
                messages.warning(request, f"Please fill the form correctly")
        
        form=PostForm()
        context = {
            "form": form,
        }
        return render(request,'blog/post_form.html',context)
    else:
        messages.warning(request, f"Only Admins are allowed")
        return redirect("blog-home")

def get_recommendations(title, indices, cosine_sim):
    df = pd.read_csv("df_pure.csv")
    idx = indices[title]
    
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:11]
    
    movie_indices = [i[0] for i in sim_scores]
    posts = []
    for name in df['name'].iloc[movie_indices]:
        posts.append(Post.objects.filter(name=name).first())
    return posts

@login_required
def PostDetailView(request,pk):
    post = get_object_or_404(Post, pk=pk)
    wl = WatchLater.objects.filter(user = request.user, name = post.name)
    if len(wl)>0:
        w_bool = True
    else:
        w_bool = False
    likes = Like.objects.filter(user = request.user, name = post.name)
    if len(likes)>0:
        l_bool = True
    else:
        l_bool = False

    if request.method== 'POST':
    
            if w_bool:
                if l_bool:
                    form=PostForm4(request.POST)
                else:
                    form=PostForm2(request.POST)
            else:
                if l_bool:
                    form=PostForm3(request.POST)
                else:
                    form=PostForm1(request.POST)

            if form.is_valid():
                ch = form.cleaned_data.get('choice')

                if ch == '1':
                    if l_bool:
                        post.likes -= 1
                        likes.delete()
                        message = f"{post.name} disliked"
                    else:
                        post.likes += 1
                        like = Like()
                        like.name = post.name
                        like.user = request.user
                        like.save()
                        message = f"{post.name} liked"
                    post.save()
                else:
                    if w_bool:
                        wl.delete()
                        message = f"{post.name} removed from your watch list"
                    else:
                        model = WatchLater()
                        model.user = request.user
                        model.name = post.name
                        model.save()
                        message = f"{post.name} added to your watch list"
                messages.success(request, message)
                return redirect('post-detail', pk)          
    else:
        if w_bool:
            if l_bool:
                form=PostForm4()
            else:
                form=PostForm2()
        else:
            if l_bool:
                form=PostForm3()
            else:
                form=PostForm1()
        df_temp = pd.read_csv("df_clean.csv")
        df = pd.read_csv("df_pure.csv")
        casts = []
        cosine_sim, indices, tfidf= vectorize(df_temp, df_temp["content"]+" "+df_temp["genres"]+" "+df_temp["country"]+" "+df_temp["cast"], df["name"])
        posts = get_recommendations(post.name, indices, cosine_sim)
        return render(request,'blog/post_detail.html', {
            "form": form,
            "post": post,
            "posts": posts,
        })

# class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Post
#     fields = ["name", "type", "genres", "rating", "director", "cast", "country", "duration", "release_date", "likes", "content"]

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)

#     def test_func(self):
#         if self.request.user.is_superuser:
#             return True
#         return False


def update_view(request, pk):
    df = pd.read_csv("df_pure.csv")
    df_temp = pd.read_csv('df_clean.csv')
    post = get_object_or_404(Post, id = pk)
    form = PostForm(request.POST or None, instance = post)
    if form.is_valid():
        post1 = WatchLater.objects.filter(name = post.name).first()
        post2 = Like.objects.filter(name = post.name).first()
        post.name = form.cleaned_data["name"]
        if post1:
            post1.name = post.name
            post1.save()
        if post2:
            post2.name = post.name
            post2.save()
        post.type = form.cleaned_data["type"]
        post.content = form.cleaned_data["content"]
        post.director = form.cleaned_data["director"]
        post.cast = form.cleaned_data["cast"]
        post.country = form.cleaned_data["country"]
        post.genres = ', '.join(form.cleaned_data["genres"])
        post.duration = form.cleaned_data["duration"]
        post.release_date = form.cleaned_data["release_date"]
        post.likes = form.cleaned_data["likes"]
        post.rating = ', '.join(form.cleaned_data["rating"])
        filt = df["name"] == post.name
        df.loc[filt, ['name', 'type', 'content', 'director', 'cast', 'country', 'genres', 'duration', 'release_date', 'likes', 'rating']] = [post.name, post.type, post.content, post.director, post.cast, post.country, post.genres, post.duration, post.release_date, post.likes, post.rating]
        new_content = sentence_engineering(post.content)
        new_name = sent_eng(post.name)
        new_cast = sent_eng(post.cast)
        new_director = sent_eng(post.director)
        df_temp.loc[filt, ['name', 'type', 'content', 'director', 'cast', 'country', 'genres', 'duration', 'release_date', 'likes', 'rating']] = [new_name, post.type, new_content, new_director, new_cast, post.country, post.genres, post.duration, post.release_date, post.likes, post.rating]
        cosine_sim, indices, tfidf = vectorize(df_temp, df_temp["name"]+" "+df_temp["cast"]+" "+df_temp["country"]+" "+df_temp["genres"], df["name"])
        joblib.dump(tfidf, "vectorizer.pkl")
        post.save()
        
        df.to_csv('df_pure.csv')
        df_temp.to_csv('df_clean.csv')

        messages.success(request, f'Entry Updated')
        return redirect('post-detail', pk) 
  
    # add form dictionary to context
    context = {
        "form": form,
    }
  
    return render(request,'blog/post_form.html',context)

# class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     model = Post
#     success_url = '/'
#     def test_func(self):
#         if self.request.user.is_superuser:
#             return True
#         return False

def delete_view(request, pk):
    df = pd.read_csv("df_pure.csv")
    df_temp = pd.read_csv('df_clean.csv')
    post_set = Post.objects.filter(id=pk)
    post = post_set.first()
    form = PostDeleteForm(request.POST or None)
    if form.is_valid():
        filt = df["name"] != post.name
        post1 = WatchLater.objects.filter(name = post.name).first()
        post2 = Like.objects.filter(name = post.name).first()
        df = df[filt]
        df_temp = df_temp[filt]
        post_set.delete()
        if post1:
            post1.delete()
        if post2:
            post2.delete()
        df.to_csv('df_pure.csv')
        df_temp.to_csv('df_clean.csv')
        messages.success(request, f'Entry Deleted')
        return redirect("blog-home")
    context = {
        "form": form,
        "post": post, 
    }
  
    return render(request,'blog/post_confirm_delete.html',context)

def watchLater(request):
    posts1 = WatchLater.objects.filter(user = request.user)
    posts2 = Like.objects.filter(user = request.user)
    liked_post = []
    for post in posts2:
        post2 = Post.objects.filter(name = post.name).first()
        liked_post.append(post2)
    watch_later = []
    for post in posts1:
        post1 = Post.objects.filter(name = post.name).first()
        watch_later.append(post1)

    # paginator = Paginator(posts, 10)
    # page = request.GET.get('page')
    # try:
    #     post_list = paginator.page(page)
    # except PageNotAnInteger:
    #     post_list = paginator.page(1)
    # except EmptyPage:
    #     post_list = paginator.page(paginator.num_pages)
    # if request.method != 'POST':
    context={
        'watch_later': watch_later,
        'liked_posts': liked_post,
    }
    return render(request, 'blog/dashboard.html',context)

def FilteredGenreView(request, cats):
    category_posts = []
    posts = Post.objects.all()
    for post in posts:
        genres = post.genres.split()
        if cats in genres:
           category_posts.append(post)
    if request.method== 'POST':
        form = Search(request.POST)
        if form.is_valid():
            cat = form.cleaned_data.get('search')
            return redirect("cat-search-genre", cats, cat)
    else:
        form = Search()
    paginator = Paginator(category_posts, 10)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    context={
        'page': page,
        # 'search_form': form,
        'post_list': post_list,
        'text': "No Movies And Shows Found",
    }
    return render(request, 'blog/index.html', context)

def GenreWatchLater(request, cats):

    category_posts = []
    posts1 = WatchLater.objects.filter(user = request.user)
    
    posts2 = Like.objects.filter(user = request.user)
    for post in posts1:
        post = Post.objects.filter(name=post.name).first()
        genres = post.genres.split()
        if cats in genres:
           category_posts.append(post)
    posts1 =category_posts
    category_posts = []
    for post in posts2:
        post = Post.objects.filter(name=post.name).first()
        genres = post.genres.split()
        if cats in genres:
           category_posts.append(post)
    posts2 =category_posts

    liked_post = []
    for post in posts2:
        post2 = Post.objects.filter(name = post.name).first()
        liked_post.append(post2)
    watch_later = []
    for post in posts1:
        post1 = Post.objects.filter(name = post.name).first()
        watch_later.append(post1)

    context={
        'watch_later': watch_later,
        'liked_posts': liked_post,
    }
    return render(request, 'blog/dashboard.html',context)
    

# def FilteredGenreView(request, cats):
#     category_posts = []
#     posts = Post.objects.all()
#     for post in posts:
#        genres = post.genres.split()
#        if cats in genres:
#            category_posts.append(post)
#     paginator = Paginator(category_posts, 10)
#     page = request.GET.get('page')
#     try:
#         post_list = paginator.page(page)
#     except PageNotAnInteger:
#         post_list = paginator.page(1)
#     except EmptyPage:
#         post_list = paginator.page(paginator.num_pages)
#     context={
#         'page': page,
#         'post_list': post_list,
#         'cats': cats
#     }

#     return render(request, 'blog/categories.html', context)


def FilteredTypeView(request, cats):
    category_posts = []
    posts = Post.objects.all().order_by("-likes")
    for post in posts:
       if post.type[0] == cats[0]:
           category_posts.append(post)
    paginator = Paginator(category_posts, 10)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    context={
        'page': page,
        'post_list': post_list,
        'cats': cats,
        'text': "No Movies And Shows Found",
    }
    return render(request, 'blog/index.html', context)

def cat_search_genre(request, cats, cat):
    category_posts = []
    posts = Post.objects.all()
    for post in posts:
        genres = post.genres.split()
        if cats in genres:
           category_posts.append(post)
    if request.method== 'POST':
        form = Search(request.POST)
        if form.is_valid():
            cat = form.cleaned_data.get('search')
            return redirect("cat-search-genre", cats, cat)
    else:
        form = Search()
    category_posts  = search(category_posts, cat)
    paginator = Paginator(category_posts, 10)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    context={
        'page': page,
        'post_list': post_list,
        'search_form': form,
    }
    return render(request, 'blog/index.html', context)