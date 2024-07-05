from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Tag, Post, Comment, Bookmark
from .serializers import TagSerializer, PostSerializer, CommentSerializer,BookmarkSerializer
from users.models import User

from rest_framework.decorators import api_view, permission_classes,APIView
from rest_framework.permissions import AllowAny,IsAuthenticated

class TagList(APIView):
    def get(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TagDetail(APIView):
    def get(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        serializer = TagSerializer(tag)
        return Response(serializer.data)

    def put(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        serializer = TagSerializer(tag, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





class PostList(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        search_term = request.GET.get('SearchTerm', '')
        per_pages = int(request.GET.get('PerPages', 3))
        page_number = int(request.GET.get('PageNum', 1))
        is_mine = request.GET.get('isMine', 'false') == 'true'
        user_email = request.GET.get('UserEmail', None)
        sort_by = request.GET.get('SortBy', 'latest')  # 추가된 부분: 정렬 기준
        user = request.user if request.user.is_authenticated else None
        

        post_list = Post.objects.all()

        if search_term:
            post_list = post_list.filter(Q(title__icontains=search_term) | Q(content__icontains=search_term))
        #특정 사용자 필터링
        if user_email:
            user_filter = get_object_or_404(User, email=user_email)
            post_list = post_list.filter(user=user_filter)
        elif is_mine and user:
            post_list = post_list.filter(user=user)
        paginator = Paginator(post_list, per_pages)

        try:
            posts = paginator.page(page_number)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        serializer = PostSerializer(posts, many=True)

        # 정렬 추가!
        if sort_by == 'latest':
            post_list = post_list.order_by('-created_at')
        elif sort_by == 'relevance' and search_term:
            post_list = post_list.annotate(
                search_rank=(
                    Q(title__icontains=search_term) * 2 +
                    Q(content__icontains=search_term)
                )
            ).order_by('-search_rank', '-created_at')
        else:
            post_list = post_list.order_by('-created_at')

        paginator = Paginator(post_list, per_pages)

        try:
            posts = paginator.page(page_number)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        serializer = PostSerializer(posts, many=True)

        #북마크 여부 및 본인 글인지 여부
        serialized_data = serializer.data
        if user:
            for post_data in serialized_data:
                post_id = post_data['id']
                post_data['is_bookmarked'] = Bookmark.objects.filter(user=user, post_id=post_id).exists()
                post_data['is_mine'] = post_list.filter(pk=post_id, author=user).exists()

        #총 페이지수, 전체 게시물 수
        return Response({
            'posts' : serialized_data,
            'pages' : paginator.num_pages,
            'total_count' : paginator.count
        })

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetail(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]  # 기본 권한을 설정하거나 다른 권한 클래스를 설정합니다.


    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentList(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetail(APIView):
    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class BookmarkList(APIView):
    def get(self, request):
        bookmarks = Bookmark.objects.all()
        serializer = BookmarkSerializer(bookmarks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookmarkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookmarkDetail(APIView):
    def get(self, request, pk):
        bookmark = get_object_or_404(Bookmark, pk=pk)
        serializer = BookmarkSerializer(bookmark)
        return Response(serializer.data)

    def put(self, request, pk):
        bookmark = get_object_or_404(Bookmark, pk=pk)
        serializer = BookmarkSerializer(bookmark, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        bookmark = get_object_or_404(Bookmark, pk=pk)
        bookmark.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)