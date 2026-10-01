# Python Camera GUI

PySide6 화면에서 RTSP 영상을 표시하고 ONVIF 카메라 제어를 연결하는 Python 프로젝트입니다. OpenCV 수신, 카메라 설정, PTZ와 객체 검출 관련 실험 코드를 포함합니다.

## 구성

- [Rtsp](Rtsp): OpenCV 영상 수신과 화면 전달
- [Onvif](Onvif): ONVIF 서비스 생성, PTZ와 스트림 주소 처리
- [Ui](Ui): GUI 관련 파일
- [ObjectDetection.py](ObjectDetection.py): 객체 검출 실험 코드
- [requirements.txt](requirements.txt): 의존성 목록

## 실행 준비

Python, PySide6, OpenCV, ONVIF 관련 패키지와 실제 카메라 설정이 필요합니다. 진입 파일 이름은 공백이 포함된 `main .py`입니다.

```bash
python -m pip install -r requirements.txt
python "main .py"
```

실행 전에 설정 파일과 WSDL 경로, 모델 경로를 맞춰야 합니다. 저장소의 YOLO 관련 모델·유틸리티는 외부 구현에 기반하므로 원본의 이용 조건을 확인해야 합니다. 독자적인 객체 검출 알고리즘을 개발했다는 의미의 저장소는 아닙니다.
