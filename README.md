# 일비 : 늘 가까이에서 도움이 되는 사람

![image](https://github.com/bokyung39/ilbi/assets/72790694/bfe1a3be-c426-49b5-9060-ba0467d9d961)


독거노인분들을 위한 낙상 감지 시스템

<br>

## 📅 프로젝트 기간

2022년 2월 - 2023년 9월

<br>

## 🌟 프로젝트 개요

- 늘 가까이에 있으면서 도움이 되는 사람, ‘일비’는 노인의 낙상을 감지하는 기기와 애플리케이션 서비스를 통해 빠른 대처와 사고 예방에 도움을 줄 수 있는 낙상 감지 시스템입니다
- 라즈베리파이를 통해 카메라의 영상을 실시간으로 분석해 낙상을 감지했을 경우 보호자에게 알림을 보냄으로써 혼자 거주하는 노인에게 낙상사고가 발생했을 시 빠르게 대처할 수 없었던 문제를 해결하고자 하였습니다

<br>

## ✨ 프로젝트 핵심 기능

### 🫧 S/W 기능

#### ‼️ 낙상 감지
- PoseNet에서 추출한 골격데이터를 이용한 낙상 감지 알고리즘을 통해 낙상 여부를 판별합니다

#### 👀 실시간 모니터링
- 앱에서 실시간으로 피보호자의 상황을 확인할 수 있습니다

#### ⛑️ 긴급 호출
- 낙상 감지 시 119에 긴급 신고 문자를 전송하는 기능을 제공합니다

####  📋 낙상 사고 기록
- 낙상 사고 발생 날짜와 시간을 포함한 낙상 사고 기록을 최신순으로 앱에서 확인 할 수 있습니다
  
### ⚡️ H/W 기능

####  📟 낙상 감지 기기
- 라즈베리파이4에 파이카메라와 적외선 센서, coral usb accelerator를 부착한 기기입니다
- coral usb accelerator를 이용해 낙상 감지 속도를 가속화하였습니다
- 카메라에 적외선 센서를 부착하여 야간 시에도 낙상 감지가 가능합니다

<br>

## 🎵 서비스 화면

### 🎺 로그인, 회원가입 페이지

<img width="710" alt="image" src="https://github.com/bokyung39/ilbi/assets/72790694/e89b5fb9-9013-4305-b4af-405d0c82b611">


### 🎸 주요 기능 페이지 - 실시간 모니터링, 긴급호출, 낙상기록 확인

<img width="714" alt="image" src="https://github.com/bokyung39/ilbi/assets/72790694/042b369e-5292-4d34-810a-9c38f31964d9">


### 💿 푸시 알림 전송

<img width="732" alt="image" src="https://github.com/bokyung39/ilbi/assets/72790694/6cc519c0-e1c8-45de-9d0d-c7607684cbab">

<br>

## 🔨 주요 기술

**Programming Language**
<div>
  <img src="https://img.shields.io/badge/java-007396?style=for-the-badge&logo=OpenJDK&logoColor=white">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white">
</div>
<br>

**App**
<div>
  <img src="https://img.shields.io/badge/androidstudio-3DDC84?style=for-the-badge&logo=androidstudio&logoColor=white">
  <img src="https://img.shields.io/badge/firebase-FFCA28?style=for-the-badge&logo=firebase&logoColor=white">
</div>
<br>

**Fall-down Detection Device**
<div>
  <img src="https://img.shields.io/badge/raspberrypi-A22846?style=for-the-badge&logo=raspberrypi&logoColor=white">
  <img src="https://img.shields.io/badge/googleCoral-ff5e4d?style=for-the-badge&logo=google&logoColor=white">
</div>

<br>
<br>


**PoseNet**
- Google에서 공개한 MobileNet 기반의 real-time pose estimation이 가능한 	AI로, RGB 형태의 입력을 CNN Model에 넣고, poses, pose confidence scores, keypoint positions, keypoint confidence scores 등의 여러 output들을 얻습니다. 이러한 output으로 PoseNet은 17개의 관절에 대한 keypoint를 추출합니다.

<br>

**낙상 감지 알고리즘**

<img width="1240" alt="image" src="https://github.com/bokyung39/ilbi/assets/72790694/6fd07bf8-86b5-4988-881f-4cc73ffb7fd2">

<br>
<br>

- 천천히 눕는 상황(낙상이 아닐 경우) <br>
  : 임계속도를 넘지 못지 못했기 때문에 낙상이라고 판단하지 않음

![ezgif com-crop](https://github.com/bokyung39/ilbi/assets/72790694/7c60e7a8-2f12-4125-9e2d-863675c6e3b8)

- 일정시간 안에 다시 일어났을 경우 <br>
  : 스스로 일어날 수 있는 상태라면 낙상이 아니거나, 위급상황이 아니라고 판단

![5-ezgif com-crop (1)](https://github.com/bokyung39/ilbi/assets/72790694/c3f881c6-2d36-4a57-8eb3-dd4016847248)

<br>

- 일정시간 동안 낙상 자세가 유지될 경우 <br>
  : 낙상이라고 판단, 보호자에게 push알림 전송

![5-ezgif com-crop](https://github.com/bokyung39/ilbi/assets/72790694/37e005ee-95d4-4479-ae32-ec70c317522e)

<br>
<br>

## 📝 기획

- 한국소비자원의 2019년 보도자료에 따르면 노인 안전사고의 위험 원인 중 낙상사고가 56.4%를 차지했으며 발생 장소의 63.4%가 주택이었을 만큼 노인 비율이 꾸준히 증가함에 따라 노인 낙상사고 발생 빈도 또한 늘어나는 추세이고, 그에 따라 낙상사고에 대한 관심도 증가하고 있습니다
- 낙상사고 감지와 관련된 연구는 계속해서 진행되고 있지만 실제로 상용화된 사례는 많지 않고 장비를 항상 착용해야 하거나 개인이 구비하기에는 부담되는 가격이라는 점을 고려해 이러한 단점을 보완하여 낙상사고에 빠르게 대처하고 노인분들이 저렴한 비용으로 간편하게 사용할 수 있는 보편화된 낙상 감지 시스템을 만들고자 하였습니다

<br>

## 📄 아키텍처 구성도

![image](https://github.com/bokyung39/ilbi/assets/72790694/334e9285-743b-4266-ae98-f6523f66f9c9)

<br>

## 👩🏻‍💻 팀원 소개
  
| 낙상 감지 기기 | App 개발 |
| ----  | -------- |
| 김보경, 이소민, 김재린 | 이현민 |

<br>

## 🗣 협업 환경

- Discord

  - 디스코드를 통해 회의와 실시간 소통 및 협업을 진행했습니다
