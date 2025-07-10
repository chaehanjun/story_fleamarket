#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
from datetime import datetime
import qrcode
from io import BytesIO
import base64

# 세션 상태에 stories 리스트 초기화
if 'stories' not in st.session_state:
    st.session_state['stories'] = []

def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

def add_story(title, author, content, product):
    story_id = len(st.session_state['stories']) + 1
    story_url = f"https://storymarket.example.com/story/{story_id}"
    qr_code_img = generate_qr_code(story_url)
    story = {
        'id': story_id,
        'title': title,
        'author': author,
        'content': content,
        'product': product,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'qr_code': qr_code_img,
        'url': story_url
    }
    st.session_state['stories'].append(story)

# 이야기 검색 함수
def search_stories(keyword):
    if not keyword:
        return stories
    keyword_lower = keyword.lower()
    return [s for s in stories if keyword_lower in s['title'].lower() or keyword_lower in s['content'].lower() or keyword_lower in s['author'].lower() or keyword_lower in s['product'].lower()]

# Streamlit 앱 UI
st.set_page_config(page_title="이야기 플리마켓", layout="wide")
st.title('이야기 플리마켓 스토리텔링 플랫폼 with QR 코드')

menu = st.sidebar.selectbox('메뉴 선택', ['이야기 등록', '이야기 목록', '스토리 검색', '통계', '데이터 다운로드'])

if menu == '이야기 등록':
    st.header('이야기 등록')
    with st.form('story_form'):
        title = st.text_input('제목')
        author = st.text_input('작성자')
        product = st.text_input('상품명 (선택)')
        content = st.text_area('이야기 내용')
        submitted = st.form_submit_button('등록')
        if submitted:
            if title and author and content:
                add_story(title, author, content, product)
                st.success('이야기가 등록되었습니다!')
            else:
                st.error('제목, 작성자, 이야기 내용은 필수 입력입니다.')

elif menu == '이야기 목록':
    st.header('등록된 이야기 목록')
    if stories:
        for story in reversed(stories):
            st.subheader(f"{story['title']} - {story['author']}")
            st.write(story['content'])
            if story['product']:
                st.write(f"상품명: {story['product']}")
            st.write(f"등록일: {story['created_at']}")
            st.markdown(f"![QR 코드](data:image/png;base64,{story['qr_code']})")
            st.write(f"QR 코드 링크: {story['url']}")
            st.markdown('---')
    else:
        st.info('등록된 이야기가 없습니다.')

elif menu == '스토리 검색':
    st.header('스토리 검색')
    keyword = st.text_input('검색어 입력')
    results = search_stories(keyword)
    if results:
        for story in results:
            st.subheader(f"{story['title']} - {story['author']}")
            st.write(story['content'])
            if story['product']:
                st.write(f"상품명: {story['product']}")
            st.write(f"등록일: {story['created_at']}")
            st.markdown(f"![QR 코드](data:image/png;base64,{story['qr_code']})")
            st.write(f"QR 코드 링크: {story['url']}")
            st.markdown('---')
    else:
        st.info('검색 결과가 없습니다.')

elif menu == '통계':
    st.header('이야기 플리마켓 통계')
    st.write(f"총 등록 이야기 수: {len(stories)}")
    if stories:
        df = pd.DataFrame(stories)
        st.bar_chart(df['author'].value_counts())
        st.bar_chart(df['product'].value_counts())
    else:
        st.info('통계 데이터가 없습니다.')

elif menu == '데이터 다운로드':
    st.header('이야기 데이터 다운로드')
    if stories:
        df = pd.DataFrame(stories)
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("CSV 다운로드", data=csv, file_name='stories.csv', mime='text/csv')
    else:
        st.info('다운로드할 데이터가 없습니다.')

