// js/main.js

document.addEventListener('DOMContentLoaded', () => {
    // 1. Sticky Navbar & Active Link Update on Scroll
    const navbar = document.getElementById('navbar');
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.nav-link');

    window.addEventListener('scroll', () => {
        // Sticky Navbar
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }

        // Active Link
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            // 네비게이션 바 높이 고려
            if (scrollY >= (sectionTop - 150)) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });

    // 2. Mobile Menu Toggle
    const mobileToggle = document.getElementById('mobile-toggle');
    const navLinksContainer = document.getElementById('nav-links');

    mobileToggle.addEventListener('click', () => {
        navLinksContainer.classList.toggle('active');
        const icon = mobileToggle.querySelector('i');
        if (navLinksContainer.classList.contains('active')) {
            icon.classList.remove('ph-list');
            icon.classList.add('ph-x');
        } else {
            icon.classList.remove('ph-x');
            icon.classList.add('ph-list');
        }
    });

    // 메뉴 클릭 시 모바일 메뉴 닫기
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            navLinksContainer.classList.remove('active');
            const icon = mobileToggle.querySelector('i');
            icon.classList.remove('ph-x');
            icon.classList.add('ph-list');
        });
    });

    // 3. Scroll Animation (Intersection Observer)
    const fadeElements = document.querySelectorAll('.fade-up');
    
    const fadeOptions = {
        threshold: 0.1,
        rootMargin: "0px 0px -50px 0px"
    };

    const fadeObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target); // 한 번만 애니메이션 실행
            }
        });
    }, fadeOptions);

    fadeElements.forEach(element => {
        fadeObserver.observe(element);
    });

    // 4. Contact Form Submission (Google Apps Script API)
    const contactForm = document.getElementById('contact-form');
    const formSuccess = document.getElementById('form-success');
    
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault(); // 기본 새로고침 방지
            
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            
            submitBtn.innerHTML = '<i class="ph ph-spinner ph-spin"></i> 전송 중...';
            submitBtn.disabled = true;

            const formData = new FormData(contactForm);
            
            // 구글 스크립트에서 이메일 필드를 인식하지 못하는 현상을 방지하기 위해, 
            // 메시지(message) 내용의 맨 앞에 이메일 주소를 명시적으로 추가합니다.
            const emailVal = formData.get('email');
            if (emailVal) {
                const originalMsg = formData.get('message') || '';
                formData.set('message', `[회신받을 이메일: ${emailVal}]\n\n${originalMsg}`);
            }
            
            // 사용자님의 구글 앱스 스크립트 웹앱 주소
            const scriptURL = 'https://script.google.com/macros/s/AKfycbwRtqq3Pc86Hms9SqiYz_kY7igEJXBkn0OBCQJ_S3BmVkyLc-hw3Lo1JyDaIN0g-_KCoQ/exec';

            // CORS 문제 방지를 위해 mode: 'no-cors' 사용
            fetch(scriptURL, { 
                method: 'POST', 
                body: formData, 
                mode: 'no-cors' 
            })
            .then(() => {
                contactForm.style.display = 'none';
                if (formSuccess) formSuccess.style.display = 'flex';
                
                // 사내 게시판 자동 등록 로직
                try {
                    const nameVal = formData.get('name') || '익명';
                    const phoneVal = formData.get('phone') || '없음';
                    const emailValStr = formData.get('email') || '없음';
                    const typeVal = formData.get('type') || '기타 문의';
                    const msgVal = formData.get('message') || ''; // 이미 [회신받을 이메일: ...] 문구가 병합되어 있음
                    
                    const boardTitle = `[웹사이트 문의 접수] ${typeVal} - ${nameVal}`;
                    const boardContent = `고객명/회사명: ${nameVal}\n연락처: ${phoneVal}\n이메일: ${emailValStr}\n문의유형: ${typeVal}\n\n[문의내용]\n${msgVal}`;
                    
                    const t = new Date();
                    const dateStr = t.getFullYear() + '-' + String(t.getMonth() + 1).padStart(2, '0') + '-' + String(t.getDate()).padStart(2, '0');
                    const newId = boardData.length > 0 ? Math.max(...boardData.map(d => d.id)) + 1 : 1;
                    
                    const newItem = {
                        id: newId,
                        title: boardTitle,
                        content: boardContent,
                        author: "시스템 자동등록",
                        date: dateStr,
                        fileName: ""
                    };
                    boardData.push(newItem);
                    localStorage.setItem('boardData', JSON.stringify(boardData));
                    if(typeof renderBoard === 'function') {
                        renderBoard();
                    }
                } catch (err) {
                    console.error("사내 게시판 등록 실패:", err);
                }
            })
            .catch(error => {
                console.error('Error!', error);
                alert('전송 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.');
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            });
        });
    }



    // 6. Reference Modal Logic
    const refBtn = document.getElementById('btn-reference');
    const refModal = document.getElementById('ref-modal');
    const refModalClose = document.getElementById('ref-modal-close');
    const refModalOverlay = document.querySelector('.ref-modal-overlay');

    if (refBtn && refModal) {
        // Open modal
        refBtn.addEventListener('click', (e) => {
            e.preventDefault();
            refModal.classList.add('active');
            document.body.style.overflow = 'hidden'; // Prevent background scrolling
        });

        // Close modal
        const closeRefModal = () => {
            refModal.classList.remove('active');
            document.body.style.overflow = '';
        };

        if (refModalClose) refModalClose.addEventListener('click', closeRefModal);
        if (refModalOverlay) refModalOverlay.addEventListener('click', closeRefModal);
        
        // Close on Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && refModal.classList.contains('active')) {
                closeRefModal();
            }
        });
    }
});

// Certificate Modal Global Functions
window.openCertModal = function(imgSrc) {
    const modal = document.getElementById('cert-modal');
    const modalImg = document.getElementById('cert-modal-img');
    const downloadBtn = document.getElementById('cert-download-btn');
    if (modal && modalImg) {
        modalImg.src = imgSrc;
        if (downloadBtn) {
            downloadBtn.href = imgSrc;
        }
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
};

window.closeCertModal = function() {
    const modal = document.getElementById('cert-modal');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
};

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        window.closeCertModal();
    }
});

// Achievement Toggle Logic
document.addEventListener('DOMContentLoaded', () => {
    const btnToggle = document.getElementById('btn-toggle-achievements');
    if (btnToggle) {
        btnToggle.addEventListener('click', () => {
            const hiddenItems = document.querySelectorAll('.timeline-item.hidden-achievement, .timeline-item.shown-achievement');
            let isShowingAll = btnToggle.innerText.includes('접기');
            
            if (isShowingAll) {
                // Hide them
                hiddenItems.forEach(item => {
                    item.classList.remove('shown-achievement');
                    item.classList.add('hidden-achievement');
                    item.style.display = 'none';
                });
                btnToggle.innerText = '더보기 (▼)';
            } else {
                // Show them
                hiddenItems.forEach(item => {
                    item.classList.remove('hidden-achievement');
                    item.classList.add('shown-achievement');
                    item.style.display = 'block';
                });
                btnToggle.innerText = '접기 (▲)';
            }
        });
    }
});

// PDF Modal Logic
window.openPdfModal = function(pdfUrl) {
    const modal = document.getElementById('pdf-modal');
    const iframe = document.getElementById('pdf-modal-iframe');
    const title = document.getElementById('pdf-modal-title');
    
    if (modal && iframe) {
        // extract filename for title
        let filename = pdfUrl.split('/').pop().replace('.pdf', '');
        filename = decodeURIComponent(filename);
        if (title) title.innerText = filename;
        
        iframe.src = pdfUrl;
        const downloadBtn = document.getElementById('pdf-download-btn');
        if(downloadBtn) downloadBtn.href = pdfUrl;
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
};

window.closePdfModal = function() {
    const modal = document.getElementById('pdf-modal');
    const iframe = document.getElementById('pdf-modal-iframe');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
        if (iframe) iframe.src = '';
    }
};

// 사내 시스템 패스워드 모달
function openPwModal() {
    document.getElementById('pw-modal-overlay').style.display = 'flex';
    document.getElementById('system-pw-input').value = '';
    document.getElementById('pw-error-msg').style.display = 'none';
    document.getElementById('system-pw-input').focus();
}

function closePwModal() {
    document.getElementById('pw-modal-overlay').style.display = 'none';
}

function checkPassword() {
    const pwInput = document.getElementById('system-pw-input').value;
    const errorMsg = document.getElementById('pw-error-msg');
    
    if (pwInput === 'ba12') {
        closePwModal();
        openInternalModal();
    } else {
        errorMsg.style.display = 'block';
    }
}

function openInternalModal() {
    document.getElementById('internal-modal-overlay').style.display = 'flex';
}

function closeInternalModal() {
    document.getElementById('internal-modal-overlay').style.display = 'none';
}

// 오버레이 클릭 시 닫기 기능 추가 (옵션)
window.addEventListener('click', function(event) {
    const pwOverlay = document.getElementById('pw-modal-overlay');
    const internalOverlay = document.getElementById('internal-modal-overlay');
    if (event.target === pwOverlay) {
        closePwModal();
    }
    if (event.target === internalOverlay) {
        closeInternalModal();
    }
    const addressOverlay = document.getElementById('address-modal-overlay');
    if (event.target === addressOverlay) {
        closeAddressBook();
    }
});

function openAddressBook() {
    document.getElementById('address-modal-overlay').style.display = 'flex';
}
function closeAddressBook() {
    document.getElementById('address-modal-overlay').style.display = 'none';
}

// --- 사내 공지사항 게시판 로직 ---

let boardData = JSON.parse(localStorage.getItem('boardData')) || [
    {
        id: 1,
        title: "신규 사내 시스템 오픈 안내",
        content: "임직원 여러분,\n금일부터 신규 사내 시스템이 오픈되었습니다.\n게시판과 주소록 기능을 적극 활용해주시기 바랍니다.\n\n감사합니다.",
        author: "관리자",
        date: "2026-06-09",
        fileName: ""
    }
];

function renderBoard() {
    const tbody = document.getElementById('board-list-body');
    if(!tbody) return;
    
    tbody.innerHTML = '';
    
    // Sort by id descending (newest first)
    const sortedData = [...boardData].sort((a, b) => b.id - a.id);
    
    if(sortedData.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" style="padding:30px; color:#999;">등록된 공지사항이 없습니다.</td></tr>';
        return;
    }
    
    sortedData.forEach(item => {
        const tr = document.createElement('tr');
        tr.className = 'board-row';
        tr.onclick = () => {
            if (isSelectMode) {
                openDeleteConfirm(item.id);
            } else {
                openBoardDetail(item.id);
            }
        };
        
        tr.innerHTML = `
            <td>${item.id}</td>
            <td style="text-align:left; padding-left:20px; font-weight:500;">${item.title} ${item.fileName ? '<i class="ph-fill ph-paperclip text-muted" style="font-size:0.9rem;"></i>' : ''}</td>
            <td>${item.author}</td>
            <td>${item.date}</td>
        `;
        tbody.appendChild(tr);
    });
}

function openBoardList() {
    renderBoard();
    document.getElementById('board-list-modal-overlay').style.display = 'flex';
}

function closeBoardList() {
    document.getElementById('board-list-modal-overlay').style.display = 'none';
}

function openBoardCreate() {
    document.getElementById('board-title-input').value = '';
    document.getElementById('board-content-input').value = '';
    document.getElementById('board-file-input').value = '';
    document.getElementById('board-create-modal-overlay').style.display = 'flex';
}

function closeBoardCreate() {
    document.getElementById('board-create-modal-overlay').style.display = 'none';
}

function submitBoard() {
    const title = document.getElementById('board-title-input').value.trim();
    const content = document.getElementById('board-content-input').value.trim();
    const fileInput = document.getElementById('board-file-input');
    
    if(!title || !content) {
        alert("제목과 내용을 모두 입력해주세요.");
        return;
    }
    
    let fileName = "";
    if(fileInput.files.length > 0) {
        fileName = fileInput.files[0].name;
    }
    
    const today = new Date();
    const dateStr = today.getFullYear() + '-' + String(today.getMonth() + 1).padStart(2, '0') + '-' + String(today.getDate()).padStart(2, '0');
    
    const newId = boardData.length > 0 ? Math.max(...boardData.map(d => d.id)) + 1 : 1;
    
    const newItem = {
        id: newId,
        title: title,
        content: content,
        author: "임직원",
        date: dateStr,
        fileName: fileName
    };
    
    boardData.push(newItem);
    localStorage.setItem('boardData', JSON.stringify(boardData));
    
    closeBoardCreate();
    renderBoard();
}

function openBoardDetail(id) {
    const item = boardData.find(d => d.id === id);
    if(!item) return;
    
    document.getElementById('detail-title').innerText = item.title;
    document.getElementById('detail-author').innerText = item.author;
    document.getElementById('detail-date').innerText = item.date;
    document.getElementById('detail-content').innerText = item.content;
    
    const fileArea = document.getElementById('detail-file-area');
    const fileNameSpan = document.getElementById('detail-file-name');
    
    if(item.fileName) {
        fileArea.style.display = 'block';
        fileNameSpan.innerText = item.fileName;
        fileNameSpan.onclick = () => alert("가상 첨부파일 다운로드 시뮬레이션입니다.");
    } else {
        fileArea.style.display = 'none';
    }
    
    document.getElementById('board-detail-modal-overlay').style.display = 'flex';
}

function closeBoardDetail() {
    document.getElementById('board-detail-modal-overlay').style.display = 'none';
}

document.addEventListener('DOMContentLoaded', () => {
    // Add overlay click events for board
    const overlays = ['board-list-modal-overlay', 'board-create-modal-overlay', 'board-detail-modal-overlay', 'board-delete-modal-overlay', 'notebook-menu-modal-overlay', 'prompt-guide-modal-overlay'];
    overlays.forEach(id => {
        const el = document.getElementById(id);
        if(el) {
            el.addEventListener('click', (e) => {
                if(e.target.id === id) {
                    if(id === 'board-list-modal-overlay') closeBoardList();
                    if(id === 'board-create-modal-overlay') closeBoardCreate();
                    if(id === 'board-detail-modal-overlay') closeBoardDetail();
                    if(id === 'board-delete-modal-overlay') closeDeleteConfirm();
                    if(id === 'notebook-menu-modal-overlay') closeNotebookMenu();
                    if(id === 'prompt-guide-modal-overlay') closePromptGuide();
                }
            });
        }
    });
});


let isSelectMode = false;
let deleteTargetId = null;

function toggleSelectMode() {
    isSelectMode = !isSelectMode;
    const btn = document.getElementById('btn-board-select-mode');
    
    if (isSelectMode) {
        btn.innerText = '취소';
        btn.style.background = '#dc3545'; // red to indicate delete mode
        btn.style.borderColor = '#dc3545';
        document.getElementById('board-list-body').style.cursor = 'crosshair';
        alert("선택 모드가 켜졌습니다. 삭제할 공지사항을 클릭해주세요.");
    } else {
        btn.innerText = '선택';
        btn.style.background = 'rgba(255,255,255,0.2)';
        btn.style.borderColor = 'rgba(255,255,255,0.5)';
        document.getElementById('board-list-body').style.cursor = 'default';
    }
}

// We need to overwrite renderBoard() to handle isSelectMode
// Since we appended renderBoard() earlier, we can just redefine it (or replace the string in the file).
// It's safer to read and replace the old renderBoard function in main.js.


function openDeleteConfirm(id) {
    deleteTargetId = id;
    document.getElementById('board-delete-modal-overlay').style.display = 'flex';
}

function closeDeleteConfirm() {
    deleteTargetId = null;
    document.getElementById('board-delete-modal-overlay').style.display = 'none';
}

function confirmDeleteBoard() {
    if (deleteTargetId !== null) {
        boardData = boardData.filter(item => item.id !== deleteTargetId);
        localStorage.setItem('boardData', JSON.stringify(boardData));
        closeDeleteConfirm();
        renderBoard();
        
        // Disable select mode after deletion for safety
        if(isSelectMode) toggleSelectMode();
    }
}


function openNotebookMenu() {
    document.getElementById('notebook-menu-modal-overlay').style.display = 'flex';
}

function closeNotebookMenu() {
    document.getElementById('notebook-menu-modal-overlay').style.display = 'none';
}

function openPromptGuide() {
    // 프롬프트 가이드 열 때 이전 메뉴 닫기
    closeNotebookMenu();
    document.getElementById('prompt-guide-modal-overlay').style.display = 'flex';
}

function closePromptGuide() {
    document.getElementById('prompt-guide-modal-overlay').style.display = 'none';
}


document.addEventListener('DOMContentLoaded', () => {
    // --- 홍보영상 컨트롤 로직 ---
    const promoVideo = document.getElementById('promo-video');
    const btnPlay = document.getElementById('btn-video-play');
    const btnPause = document.getElementById('btn-video-pause');

    if (promoVideo && btnPlay && btnPause) {

        // 자동 재생 (화면에 보일 때)
        if ('IntersectionObserver' in window) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        promoVideo.play().then(() => {
                            btnPlay.style.display = 'none';
                            btnPause.style.display = 'inline-block';
                        }).catch(e => console.log('Autoplay prevented:', e));
                    } else {
                        promoVideo.pause();
                        btnPause.style.display = 'none';
                        btnPlay.style.display = 'inline-block';
                    }
                });
            }, { threshold: 0.5 });
            observer.observe(promoVideo);
        }

        btnPlay.addEventListener('click', () => {
            promoVideo.play();
            btnPlay.style.display = 'none';
            btnPause.style.display = 'inline-block';
        });

        btnPause.addEventListener('click', () => {
            promoVideo.pause();
            btnPause.style.display = 'none';
            btnPlay.style.display = 'inline-block';
        });
    }
});


// 카드뉴스 슬라이더 기능
let currentSlide = 0;
window.moveSlide = function(direction) {
    const track = document.getElementById('card-slider-track');
    if (!track) return;
    const totalSlides = 5;
    currentSlide += direction;
    if (currentSlide < 0) currentSlide = totalSlides - 1;
    if (currentSlide >= totalSlides) currentSlide = 0;
    track.style.transform = `translateX(-${currentSlide * 100}%)`;
};
