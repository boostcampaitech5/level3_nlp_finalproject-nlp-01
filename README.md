![header](https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=1&height=250&section=header&text=TexTuneS%20:%20Make%20Your%20Creative%20Music&fontSize=40)

<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/amazonaws-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white"> 
<img src="https://img.shields.io/badge/pytorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white">
<img src="https://img.shields.io/badge/streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white">
<img src="https://img.shields.io/badge/fastapi-009688?style=for-the-badge&logo=fastapi&logoColor=white">
<img src="https://img.shields.io/badge/githubactions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white">
<img src="https://img.shields.io/badge/transformers-FFFF33?style=for-the-badge">

# TexTuneS
누구나 쉽고 간단하게 적합한 나만의 배경 음악을 만들어 제공해주는 웹서비스 입니다.  
[발표 자료](https://github.com/boostcampaitech5/level3_nlp_finalproject-nlp-01/blob/main/assets/final_project_Presentation.pdf)|
[발표 영상](https://youtu.be/LWodtP5Kh6Q) | 
[데모 사이트](http://101.101.209.53:30007/)  


## 프로젝트 소개
### 크리에이터를 위한 맞춤형 음악 생성 서비스

배경음악은 우리가 의식하지 않아도 우리의 감정, 사고, 행동을 조정하는 힘을 가지고 있으며 다양한 경험들 속에서 영향력을 끼치고 있습니다.

또한 다양한 컨텐츠 속에서 배경음악은 이미 많이 활용되고 있으며, 이는 더 대상에 관심을 가지게 하며 상황에 더 몰입할 수 있는 환경을 제공하고 있습니다.

**TexTunes**는 **다양한 컨텐츠에 적합하게 활용할 수 있는 배경음악**을 만들고 싶은 모든 크리에이터들을 위해 누구나 **쉽고** **간단**하게 나만의 맞춤형 배경음악을 만들어주는 경험을 제공합니다.

음악 생성 모델을 활용하여 배경음악을 만들고 **더 완성도 높은 컨텐츠**를 만들어 보세요.

---
![image](https://github.com/boostcampaitech5/level3_nlp_finalproject-nlp-01/assets/39620398/53dcb7bf-9308-46ef-bb87-084f4311b2a8)

---

![image](https://github.com/boostcampaitech5/level3_nlp_finalproject-nlp-01/assets/39620398/1dc68299-3c37-4bc4-87ff-757204d54776)


## 팀 소개
### Boostcamp AI-Tech 5기 NLP-01조 자만추
| 팀원| 작업|
| --- | --- |
| [김효연_T5072](https://github.com/Broco98) | Streamlit 프론트엔드, llama2 모델 구현 및 프롬프트 엔지니어링 |
| [서유현_T5107](https://github.com/a-Tachyon) | 데이터 수집, 음악 생성 모델 구현 및 fine tuning 등 성능 개선 |
| [손무현_T5114](https://github.com/MuHyeonSon) | 데이터 수집, 음악 생성 모델 조사 및 음악 생성 서버 구축, 카테고리 정의 및 데이터 구축  |
| [이승진_T5144](https://github.com/MonteCarlolee) | 생성 요약 모델 연구 및 논문 구현 |
| [최규빈_T5215](https://github.com/gyubinc) | 토픽 모델링, 장르 classification 모델 구현 |
| [황지원_T5231](https://github.com/Jiwonii97) | PM, Streamlit 프론트엔드, 음악 도메인 감정모델 연구 및 서빙 |

## Directory Tree
```
├── README.md
├── appspec.yml
├── fastapi # test server
│   └── main.py
├── requirements.txt
└── streamlit
    ├── assets
    │   ├── category_ver1.0.3.json
    │   ├── extra_exam.png
    │   ├── main_image.png
    │   ├── music_icon.png
    │   ├── page_icon.png
    │   ├── secret.json # secret
    │   ├── sidebar_img.png
    │   ├── simple_exam.png
    │   ├── test_music.wav
    │   └── text_exam.png
    ├── constraints
    │   ├── COMPONENT.py
    │   ├── INFO.py
    │   ├── PATH.py
    │   ├── SECRET.py
    │   └── TAG.py
    ├── demo
    │   ├── # 데모 노래
    ├── main.py
    ├── models
    │   └── Content.py
    ├── pages
    │   ├── 01_Simple_Category.py
    │   ├── 02_Extra_Category.py
    │   └── 03_Text_Analysis.py
    └── utils
        ├── api.py
        ├── attribute.py
        ├── config.py
        ├── generator.py
        └── log.py
```
## 참고 사이트

음악 생성 API: <https://github.com/boostcampaitech5/level3_nlp_productserving-nlp-01-1>  
문서 분석(문서 요약, 토픽 분류, 감정분석) API: <https://github.com/boostcampaitech5/level3_nlp_productserving-nlp-01-2>  

![Footer](https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=1&height=200&section=footer)
