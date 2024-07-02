import React from 'react';
import { Link, useParams } from 'react-router-dom';
import styled from 'styled-components';

const Container = styled.div`
  padding: 20px;
  background-color: var(--preset--color--base-2);
  border-radius: 5px;
  width: 100%;
  box-shadow: 0px 12px 16px 0 #888;
  box-sizing: border-box;
`;

const PostHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--preset--color--contrast);
  margin-bottom: 20px;
`;

const AuthorProfileImg = styled.img`
  width: 80px;
  height: 80px;
  background-color: #D9D9D9;
  border-radius: 50%;
`;

const PostTitleWrap = styled.div`
  flex: 1;
  & h1 {
    margin: unset;
    margin-bottom: 10px;
    font-size: 27px;
  }
`;

const PostInfoWrap = styled.div`
  display: flex;
  gap: 30px;
  & p {
    margin: unset;
    font-size: 14px;
    color: var(--preset--color--contrast);
  }
`;

const BookMarkIcon = styled.img`
  cursor: pointer;

  &.on {
    background-image: url("/bookmark-on.png");
  }
`;

const PostContent = styled.div`
    width: 100%;
    max-width: 800px;
    padding: 20px;
    min-height: 300px;
    box-sizing: border-box;
`;

const Attachment = styled.div`
  display: flex;
  align-items: center;
  gap: 5px;

  & img {
    width: 20px;
  }

  & p {
    margin: unset;
    font-size: 15px;
  }
`;

const PostControlBox = styled.div`
    margin-top: 20px;
    background-color: #F5FDFF;
    width: 100%;
    box-shadow: 0px 12px 16px 0 #888;
    box-sizing: border-box;
    position: fixed;
    left: 0;
    bottom: 0;
    border-top: 1px solid var(--preset--color--contrast-2);
    text-align: -webkit-center;
`;

const PostcontrolBoxInner = styled.div`
    display: flex;
    max-width: 1200px;
    padding: 10px 20px;
`;

const LikeWrap = styled.div`
    display: flex;
    align-items: center;
    gap: 10px;
    & img {
      width: 20px;
      height: 20px;
    }
`;

const CommentButtonWrap = styled.div`
  
`;

const SearchSinglePost = () => {
  const { postId } = useParams();

  return (
    <>
      <Container>
        <PostHeader>
          <AuthorProfileImg />
          <PostTitleWrap>
            <h1>게시물 제목</h1>
            <PostInfoWrap>
              <p>아무개왈</p>
              <p>24.00.00</p>
            </PostInfoWrap>
          </PostTitleWrap>
          <BookMarkIcon width="40px" height="40px" src="/bookmark.png" />
        </PostHeader>
        <PostContent>
          <p>입력한 내용~~~~~~~~~~~~~~~~~~~~~~~~</p>
        </PostContent>
        <Attachment>
          <img src='/attach.png'/>
          <p>파일첨부</p>
        </Attachment>
      </Container>
      <PostControlBox>
        <PostcontrolBoxInner>
          <LikeWrap>
            <img src='/like-empty.png'/>
            <span>1,000</span>
          </LikeWrap>
          <CommentButtonWrap>

          </CommentButtonWrap>
        </PostcontrolBoxInner>
      </PostControlBox>
    </>
  );
};

export default SearchSinglePost;