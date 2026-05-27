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
});
