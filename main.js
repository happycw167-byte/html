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

    // 4. Contact Form Submission
    const contactForm = document.getElementById('contact-form');
    const formSuccess = document.getElementById('form-success');

    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            // 폼 유효성 검사 (HTML5 required 속성으로 기본 처리됨)
            
            // 시뮬레이션: 제출 버튼 상태 변경
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="ph ph-spinner ph-spin"></i> 전송 중...';
            submitBtn.disabled = true;

            // 가상의 비동기 전송 대기 (1.5초)
            setTimeout(() => {
                // 성공 메시지 표시
                contactForm.style.display = 'none';
                formSuccess.style.display = 'flex';
                
                // 선택적: 백엔드 연동을 위해서는 여기서 fetch API 등을 사용
            }, 1500);
        });
    }

    // 5. AI Chatbot Logic (Mock)
    const chatToggle = document.getElementById('ai-chat-toggle');
    const chatWindow = document.getElementById('ai-chat-window');
    const chatClose = document.getElementById('ai-chat-close');
    const chatInput = document.getElementById('chat-input');
    const chatSendBtn = document.getElementById('chat-send');
    const chatBody = document.getElementById('chat-body');

    if (chatToggle && chatWindow) {
        // Toggle Chat Window
        chatToggle.addEventListener('click', () => {
            chatWindow.classList.add('active');
            chatInput.focus();
        });

        chatClose.addEventListener('click', () => {
            chatWindow.classList.remove('active');
        });

        // Send Message
        const sendMessage = () => {
            const text = chatInput.value.trim();
            if (!text) return;

            // Add User Message
            addMessage(text, 'user-message');
            chatInput.value = '';
            
            // Show Typing Indicator
            showTypingIndicator();

            // Get AI Response (Mock)
            setTimeout(() => {
                removeTypingIndicator();
                const response = getAIResponse(text);
                addMessage(response, 'ai-message');
            }, 1000 + Math.random() * 1000); // 1~2초 딜레이
        };

        chatSendBtn.addEventListener('click', sendMessage);
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });

        // Helper Functions
        function addMessage(text, className) {
            const msgDiv = document.createElement('div');
            msgDiv.className = `chat-message ${className}`;
            msgDiv.textContent = text;
            chatBody.appendChild(msgDiv);
            chatBody.scrollTop = chatBody.scrollHeight;
        }

        function showTypingIndicator() {
            const indicator = document.createElement('div');
            indicator.className = 'typing-indicator';
            indicator.id = 'typing-indicator';
            indicator.innerHTML = `
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            `;
            chatBody.appendChild(indicator);
            chatBody.scrollTop = chatBody.scrollHeight;
        }

        function removeTypingIndicator() {
            const indicator = document.getElementById('typing-indicator');
            if (indicator) indicator.remove();
        }

        // Mock AI Logic focusing ONLY on BEATECH
        function getAIResponse(query) {
            // 정규식으로 질문 키워드 분석
            const q = query.replace(/\s+/g, '');
            
            // 1. 인사말
            if (/안녕|반가워|하이/.test(q)) {
                return "안녕하세요! 저는 비에이텍의 펌프 시스템과 기술에 대해 안내해 드리는 AI 도우미입니다. 궁금하신 점을 말씀해 주세요.";
            }
            
            // 2. 회사 위치/주소/연락처
            if (/주소|위치|어디|연락처|전화번호|번호|팩스|이메일/.test(q)) {
                return "(주)비에이텍의 본사 및 공장은 '강원특별자치도 춘천시 퇴계공단2길 64'에 위치해 있습니다. 전화번호는 033) 264-9243, 팩스는 033) 251-5747, 이메일은 gwf0123@hanmail.com 입니다.";
            }
            
            // 3. 제품 소개
            if (/제품|부스터펌프|부스터|수직형|다단|산업용|벌류트|수중|심정용|오수|슬러지/.test(q)) {
                return "비에이텍은 위생안전기준을 통과한 지상용 수직형 다단 펌프 위주의 '부스터 펌프 시스템'과, 고성능 '산업용 펌프(벌류트, 정량, 수중, 오수/슬러지 펌프 등)'를 제조 및 판매하고 있습니다. 차별화된 인버터 제어로 고효율, 저소음을 자랑합니다.";
            }
            
            // 4. 회사 소개/대표
            if (/대표|조세연|회사|소개|비에이텍이뭐야|무슨회사|인증|KC|메인비즈|MAIN-BIZ|ISO/.test(q)) {
                return "(주)비에이텍은 조세연 대표이사가 이끄는 워터 펌프 전문 기업으로, 위생안전기준(KC), MAIN-BIZ, ISO 9001:2015 인증을 보유하고 있습니다. 차별화된 펌프 제어 및 위생 관리 기술을 제공합니다.";
            }

            // 5. 조직/부서
            if (/조직도|생산부|관리부|품질보증부|부서/.test(q)) {
                return "비에이텍은 대표이사 산하에 생산부(제품 생산, 원자재 구입), 관리부(계약 및 공정 관리), 품질보증부(품질 관리, A/S)로 구성되어 체계적으로 운영되고 있습니다.";
            }

            // 6. 비에이텍과 무관한 질문 필터링 (가장 중요한 요구사항)
            return "죄송합니다. 저는 (주)비에이텍과 관련된 질문(회사 소개, 제품 정보, 연락처 등)에만 답변할 수 있도록 설계되었습니다. 펌프 시스템이나 비에이텍에 대해 궁금하신 점을 다시 질문해 주시겠어요?";
        }
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
