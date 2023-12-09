// 비디오 스트림 및 카메라 접근
navigator.mediaDevices.getUserMedia({video: true})
    .then(function (stream) {
        let video = document.getElementById('video');
        video.srcObject = stream;
        video.play();
    })
    .catch(function (err) {
        console.error("카메라에 접근할 수 없습니다: ", err);
    });

// 사진 찍기 버튼 클릭 이벤트 핸들러
document.getElementById('capture').addEventListener('click', function () {
    let video = document.getElementById('video');
    let canvas = document.getElementById('canvas');
    let photo = document.getElementById('photo');

    // Canvas에 현재 비디오 화면을 그림
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);

    // Canvas의 이미지 데이터를 base64 형태로 가져와서 img 태그에 표시
    photo.src = canvas.toDataURL('image/png');

    // 찍은 사진을 로컬 스토리지에 저장
    localStorage.setItem('capturedPhoto', photo.src);

});