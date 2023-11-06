# '싯가 얼마?'앱을 위한 <br/> Python의 Flask로 구현한 서버 앱

## 소개
Mysql와의 연결, TensorFlow라이브러리를 통한 AI Model 분석 등          
Swift & Ract App을 위한 Flask 기반의 RESTful 및 Socketio 서버 입니다.

## 관련 PDF
<a href ="https://docs.google.com/presentation/d/1guynCM9FxU7GH3fNlxiqnO5YECwNdO_zMQWiROuSxUU/edit?usp=sharing">
    <img src = https://github.com/Oh-Kang94/SeasonFinal_Main_Server_Flask/blob/master/readme/images/PPT.png>
    <br/>             
  누르시면, 관련 PPT로 이동됩니다.
</a>

## 서버 구성도
<img src = https://github.com/Oh-Kang94/SeasonFinal_Main_Server_Flask/blob/master/readme/images/Server.png>

## API 문서
이 프로젝트의 API 문서는 Swagger UI를 통해 확인할 수 있습니다.
<a href="https://final.oh-kang.kro.kr">
    <img src = https://github.com/Oh-Kang94/SeasonFinal_Main_Server_Flask/blob/master/readme/images/SwaggerUI.png>
    <br/>             
  Swagger UI보러 가기!!
</a>    

### 간략 설명 
1. APScheduler를 이용한 서버 스케쥴로 활용한 자동화
2. SOCKET.IO를 이용한 간단한 채팅 및 경매 운영
4. JWT를 이용한 인증 방식의 보안 구성
5. uWSGI를 이용한 비동기 서버 애플리케이션 처리

### SCOKTIO 구성
<a href="https://drive.google.com/file/d/1UBy0H5HQvWN7DPqqCx3F-KMDegwKeQiC/view?usp=share_link" title="시연영상으로 이동">![image](https://github.com/Oh-Kang94/SeasonFinal_Main_Server_Flask/blob/master/readme/images/socket_image.png)시연영상으로 이동</a>      
\<Join> : Room(Auctionid)를 입장해, “Message”, “System” 이벤트를 듣게 만든다.<br>
유저가 아니라면, “System”으로 “올바른 사용자가 아님을 알림 <br>
맞다면, “{id}님이 경매에 참여하였습니다.”라는 메시지로 전체 경매자들한테 알림.<br>
ViewCount를 1 올림<br>

\<Leave> : Room(Auctionid)을 나가, 더이상 Socket 연결을 안하게 만듬.


\<message> : 
1) ‘# price:int’를 인식해, 숫자 값이면    
    1. 현 경매 최고 금액보다 높은 경우,<br> “{id}님이 {price_now}로 성공적으로 입찰하였습니다.”를 “Message”출력<br>
    Mysql에 최고 금액을 바꾸고, Buyerid도 갱신한다.<br>
    2. 낮거나 같은 경우. “{price_now}로 입찰실패하였습니다.<br> 금액을 확인 후 시도해 주세요.”를 “System” 출력
    3. 숫자가 아닌 경우 . “숫자값을 입력하세요”를  “System” 출력

2) 일반 메시지 경우,
   <br> “Message”에 ‘user’, ‘context’를 출력<br>모든 “Message” 출력은 ‘Redis’에 저장


\<getmessage> : Mysql과 Redis에서 모든 채팅 기록을 가지고, “System”에 출력해, 유저의 기존 경매정보를 확인할 수 있는 기회 제공

### 설치 방법
    pip install -r requirements.txt
    ** 실행시,
    flask run
    ** 백그라운드에서 실행시,
    nohup flask run --host=0.0.0.0    

## 기술 스택
  <img src="https://skillicons.dev/icons?i=aws,mysql,py,flask,tensorflow,nginx,redis"/>

## 저자

- [Oh-Kang](https://github.com/Oh-Kang94)
