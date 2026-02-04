// ========================================
// BizToolz AI — Main JavaScript
// ========================================

import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getFirestore, collection, addDoc, serverTimestamp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js";

// TODO: Replace with your actual Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyANp3y8MNKSwB1S_leXT2NT7DeKab9AG58",
    authDomain: "biztoolzai.firebaseapp.com",
    projectId: "biztoolzai",
    storageBucket: "biztoolzai.firebasestorage.app",
    messagingSenderId: "106172488870",
    appId: "1:106172488870:web:0fee94e6821a1059912867",
    measurementId: "G-2YNJ0HMCDY"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

document.addEventListener('DOMContentLoaded', () => {
    // Mobile menu toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            mobileMenuBtn.classList.toggle('active');
        });
    }

    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    let lastScroll = 0;
    
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 100) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        
        lastScroll = currentScroll;
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const navHeight = navbar.offsetHeight;
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - navHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
                
                // Close mobile menu if open
                navLinks.classList.remove('active');
                mobileMenuBtn.classList.remove('active');
            }
        });
    });

    // Newsletter form submission
    const newsletterForm = document.querySelector('.newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const emailInput = newsletterForm.querySelector('input[type="email"]');
            const email = emailInput.value;
            const button = newsletterForm.querySelector('button');
            const originalText = button.innerHTML;
            
            // Show loading state
            button.innerHTML = 'Subscribing...';
            button.disabled = true;
            
            try {
                // Save to Firestore
                await addDoc(collection(db, "subscribers"), {
                    email: email,
                    createdAt: serverTimestamp(),
                    source: window.location.pathname
                });

                button.innerHTML = '✓ Subscribed!';
                button.style.background = 'linear-gradient(135deg, #10b981 0%, #059669 100%)';
                emailInput.value = ''; // Clear input
                
                // Reset after 3 seconds
                setTimeout(() => {
                    button.innerHTML = originalText;
                    button.style.background = '';
                    button.disabled = false;
                }, 3000);

            } catch (error) {
                console.error("Error adding document: ", error);
                button.innerHTML = 'Error. Try again.';
                button.style.background = '#ef4444';
                
                setTimeout(() => {
                    button.innerHTML = originalText;
                    button.style.background = '';
                    button.disabled = false;
                }, 3000);
            }
        });
    }

    // Submit Tool Form Handler
    const submitToolForm = document.getElementById('submit-tool-form');
    if (submitToolForm) {
        submitToolForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const button = submitToolForm.querySelector('button');
            const originalText = button.innerHTML;
            
            button.innerHTML = 'Submitting...';
            button.disabled = true;

            const formData = {
                toolName: document.getElementById('toolName').value,
                toolUrl: document.getElementById('toolUrl').value,
                category: document.getElementById('category').value,
                pricing: document.getElementById('pricing').value,
                tagline: document.getElementById('tagline').value,
                description: document.getElementById('description').value,
                contactEmail: document.getElementById('contactEmail').value,
                affiliateProgram: document.getElementById('affiliateProgram').value,
                submittedAt: serverTimestamp(),
                status: 'pending' // pending review
            };

            try {
                await addDoc(collection(db, "tool_submissions"), formData);
                
                // Show success UI (Replace form with message)
                const container = document.querySelector('.submit-form');
                container.innerHTML = `
                    <div style="text-align: center; padding: 3rem 0;">
                        <div style="font-size: 4rem; margin-bottom: 1rem;">🎉</div>
                        <h2 style="margin-bottom: 1rem;">Submission Received!</h2>
                        <p style="color: #475569; margin-bottom: 2rem;">Thanks for submitting <strong>${formData.toolName}</strong>. Our team will review it shortly.</p>
                        <a href="/" class="btn btn-primary">Back to Home</a>
                    </div>
                `;
                
                // Optional: Trigger your own notification here if needed

            } catch (error) {
                console.error("Error submitting tool: ", error);
                button.innerHTML = 'Error. Please try again.';
                button.style.background = '#ef4444';
                
                setTimeout(() => {
                    button.innerHTML = originalText;
                    button.style.background = '';
                    button.disabled = false;
                }, 3000);
            }
        });
    }

    // Staggered animation delays for cards
    const cardTypes = [
        { selector: '.tool-card', baseDelay: 0 },
        { selector: '.comparison-card', baseDelay: 0 },
        { selector: '.guide-card', baseDelay: 0 },
        { selector: '.trust-item', baseDelay: 0 }
    ];

    cardTypes.forEach(({ selector }) => {
        document.querySelectorAll(selector).forEach((el, i) => {
            el.style.animationDelay = `${i * 100}ms`;
        });
    });

    // Animate elements on scroll with stagger
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all cards and sections
    document.querySelectorAll('.tool-card, .comparison-card, .guide-card, .trust-item').forEach(el => {
        observer.observe(el);
    });

    // Add animation class
    document.head.insertAdjacentHTML('beforeend', `
        <style>
            .animate-in {
                animation-play-state: running !important;
            }
        </style>
    `);

    // Enhanced tool card hover effects
    document.querySelectorAll('.tool-card, .comparison-card, .guide-card').forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-8px)';
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
        });
    });

    // Button press effect
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('mousedown', () => {
            btn.style.transform = 'scale(0.98)';
        });

        btn.addEventListener('mouseup', () => {
            btn.style.transform = '';
        });

        btn.addEventListener('mouseleave', () => {
            btn.style.transform = '';
        });
    });

    // Input focus glow effect
    document.querySelectorAll('input').forEach(input => {
        input.addEventListener('focus', () => {
            input.style.boxShadow = '0 0 0 3px rgba(212, 168, 83, 0.15)';
        });

        input.addEventListener('blur', () => {
            input.style.boxShadow = '';
        });
    });

    // Stats counter animation
    const stats = document.querySelectorAll('.stat-number');
    
    const animateValue = (element, start, end, duration) => {
        const range = end - start;
        const startTime = performance.now();
        
        const updateValue = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const easeProgress = 1 - Math.pow(1 - progress, 3); // easeOutCubic
            
            const current = Math.floor(start + (range * easeProgress));
            element.textContent = current + (element.dataset.suffix || '');
            
            if (progress < 1) {
                requestAnimationFrame(updateValue);
            } else {
                element.textContent = end + (element.dataset.suffix || '');
            }
        };
        
        requestAnimationFrame(updateValue);
    };

    const statsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                const text = el.textContent;
                const value = parseInt(text);
                const suffix = text.replace(/[0-9]/g, '');
                
                if (!isNaN(value)) {
                    el.dataset.suffix = suffix;
                    animateValue(el, 0, value, 2000);
                }
                
                statsObserver.unobserve(el);
            }
        });
    }, { threshold: 0.5 });

    stats.forEach(stat => statsObserver.observe(stat));

    // Add subtle parallax to hero
    const hero = document.querySelector('.hero');
    if (hero) {
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            if (scrolled < window.innerHeight) {
                hero.style.backgroundPositionY = scrolled * 0.5 + 'px';
            }
        });
    }

    console.log('✨ BizToolz AI Dark Theme loaded successfully!');
});
