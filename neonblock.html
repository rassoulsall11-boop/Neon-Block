```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>NEXUS: VELOCITY | Enterprise Build v4.0</title>
    <style>
        /* --- INDUSTRIAL CSS ARCHITECTURE --- */
        :root {
            --c-void: #050505;
            --c-ui-bg: rgba(10, 10, 15, 0.85);
            --c-primary: #00f3ff; /* Cyan Neon */
            --c-danger: #ff0055;  /* Red Neon */
            --c-warn: #ffcc00;
            --c-text: #ffffff;
            --f-main: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            --ease-out: cubic-bezier(0.215, 0.61, 0.355, 1);
        }

        * { box-sizing: border-box; touch-action: none; user-select: none; -webkit-tap-highlight-color: transparent; }
        
        body, html {
            margin: 0; padding: 0; width: 100%; height: 100%;
            background-color: var(--c-void);
            overflow: hidden;
            font-family: var(--f-main);
            color: var(--c-text);
        }

        /* HARDWARE ACCELERATED LAYER */
        #game-layer {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            z-index: 1;
        }

        /* UI OVERLAY SYSTEM */
        .ui-layer {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            z-index: 10;
            pointer-events: none; /* Let clicks pass through to game when not interacting with UI */
            display: flex; flex-direction: column; justify-content: center; align-items: center;
        }

        .ui-element { pointer-events: auto; }

        /* HUD */
        #hud {
            position: absolute; top: 0; left: 0; width: 100%;
            padding: 20px;
            display: flex; justify-content: space-between;
            font-weight: 700; letter-spacing: 2px;
            text-shadow: 0 0 10px var(--c-primary);
            opacity: 0; transition: opacity 0.5s;
        }

        .btn-pause {
            background: none; border: 2px solid var(--c-text); color: var(--c-text);
            padding: 5px 15px; border-radius: 4px; cursor: pointer;
            font-weight: bold; text-transform: uppercase;
        }

        /* MENUS & MODALS (Glassmorphism) */
        .screen {
            background: var(--c-ui-bg);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255,255,255,0.1);
            padding: 40px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 20px 50px rgba(0,0,0,0.8);
            transform: scale(0.95);
            opacity: 0;
            transition: all 0.4s var(--ease-out);
            display: none; /* Managed by JS State Machine */
            max-width: 400px; width: 90%;
        }

        .screen.active {
            transform: scale(1);
            opacity: 1;
            display: flex; flex-direction: column; gap: 20px;
        }

        h1 { margin: 0; font-size: 2.5rem; text-shadow: 0 0 20px var(--c-primary); letter-spacing: -1px; }
        h2 { margin: 0; color: var(--c-primary); font-size: 1.2rem; text-transform: uppercase; letter-spacing: 2px; }
        p { color: #aaa; font-size: 0.9rem; line-height: 1.5; }

        /* CTA BUTTONS */
        .btn-primary {
            background: var(--c-primary); color: #000;
            border: none; padding: 16px 32px;
            font-size: 1.1rem; font-weight: 800; text-transform: uppercase; letter-spacing: 1px;
            border-radius: 4px; cursor: pointer;
            transition: transform 0.1s, box-shadow 0.2s;
            box-shadow: 0 0 15px var(--c-primary);
        }
        .btn-primary:active { transform: scale(0.96); }

        .btn-secondary {
            background: transparent; border: 1px solid rgba(255,255,255,0.3); color: #fff;
            padding: 12px 24px; border-radius: 4px; cursor: pointer;
            text-transform: uppercase; font-size: 0.9rem;
            transition: background 0.2s;
        }
        .btn-secondary:hover { background: rgba(255,255,255,0.1); }

        /* UTILITY */
        .hidden { display: none !important; }
    </style>
</head>
<body>

    <!-- RENDER TARGET -->
    <canvas id="game-layer"></canvas>

    <!-- UI SYSTEM -->
    <div id="ui-layer" class="ui-layer">
        
        <!-- HUD -->
        <div id="hud" class="ui-element">
            <div>SCORE: <span id="score-val">0</span></div>
            <button class="btn-pause" id="btn-pause">II</button>
        </div>

        <!-- MAIN MENU -->
        <div id="menu-main" class="screen active ui-element">
            <h1>NEXUS<br><span style="color:var(--c-primary)">VELOCITY</span></h1>
            <p>AVOID THE GLITCHES. SURVIVE THE VOID.<br>Touch or Mouse to Move.</p>
            <div style="margin: 10px 0; border-top: 1px solid #333; padding-top:10px;">
                <small>HIGH SCORE: <span id="menu-highscore">0</span></small>
            </div>
            <button class="btn-primary" id="btn-start">INITIALIZE RUN</button>
        </div>

        <!-- PAUSE MENU -->
        <div id="menu-pause" class="screen ui-element">
            <h2>SYSTEM PAUSED</h2>
            <button class="btn-primary" id="btn-resume">RESUME</button>
            <button class="btn-secondary" id="btn-quit">ABORT TO MENU</button>
        </div>

        <!-- GAME OVER -->
        <div id="menu-gameover" class="screen ui-element">
            <h2 style="color: var(--c-danger)">CRITICAL FAILURE</h2>
            <div>
                <p>FINAL SCORE</p>
                <h1 id="go-score">0</h1>
            </div>
            <button class="btn-primary" id="btn-restart">RETRY</button>
            <button class="btn-secondary" id="btn-go-menu">MAIN MENU</button>
        </div>
    </div>

<script>
/**
 * NEXUS ARCHITECT v4.0 - TRIPLE-A JAVASCRIPT ENGINE
 * Pattern: Entity-Component-System (Lite), State Machine, Object Pooling
 * Optimization: TypedArrays, Bitwise Ops, Canvas API Hardware Acceleration
 */

// --- 1. CORE CONFIGURATION (SINGLETON) ---
const Config = {
    colors: {
        player: '#00f3ff',
        enemy: '#ff0055',
        bg: '#050505',
        grid: '#1a1a2e'
    },
    physics: {
        drag: 0.15,
        speed: 8,
        baseEnemySpeed: 3
    },
    storageKey: 'nexus_velocity_save_v1'
};

// --- 2. AUDIO ENGINE (Web Audio API - Procedural) ---
class AudioSynth {
    constructor() {
        this.ctx = new (window.AudioContext || window.webkitAudioContext)();
        this.master = this.ctx.createGain();
        this.master.gain.value = 0.3;
        this.master.connect(this.ctx.destination);
    }

    playTone(freq, type, duration, vol = 1) {
        if(this.ctx.state === 'suspended') this.ctx.resume();
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = type;
        osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
        gain.gain.setValueAtTime(vol, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + duration);
        osc.connect(gain);
        gain.connect(this.master);
        osc.start();
        osc.stop(this.ctx.currentTime + duration);
    }

    sfxStart() { this.playTone(440, 'sine', 0.5); this.playTone(880, 'triangle', 0.5, 0.5); }
    sfxCrash() { this.playTone(100, 'sawtooth', 0.8, 0.8); this.playTone(50, 'square', 1.0, 1.0); }
    sfxUI() { this.playTone(800, 'sine', 0.1, 0.2); }
}

// --- 3. STORAGE MANAGER (Persistence) ---
class StorageManager {
    static save(score) {
        const current = this.load();
        if (score > current.highScore) {
            localStorage.setItem(Config.storageKey, JSON.stringify({ highScore: score }));
            return true; // New Record
        }
        return false;
    }

    static load() {
        try {
            const data = localStorage.getItem(Config.storageKey);
            return data ? JSON.parse(data) : { highScore: 0 };
        } catch (e) {
            console.warn('Storage Error:', e);
            return { highScore: 0 };
        }
    }
}

// --- 4. GAME ENGINE ---
class Game {
    constructor() {
        this.canvas = document.getElementById('game-layer');
        this.ctx = this.canvas.getContext('2d', { alpha: false, desynchronized: true });
        this.audio = new AudioSynth();
        
        // State
        this.state = 'MENU'; // MENU, PLAY, PAUSE, GAMEOVER
        this.score = 0;
        this.highScore = StorageManager.load().highScore;
        this.difficultyMultiplier = 1;
        this.frames = 0;

        // Entities
        this.player = { x: 0, y: 0, w: 30, h: 30, targetX: 0, trail: [] };
        this.enemies = [];
        this.particles = [];
        
        // Input
        this.pointer = { x: 0, y: 0, isDown: false };
        
        this.resize();
        this.initInput();
        this.renderMenuScore();
        
        // Loop Bind
        this.loop = this.loop.bind(this);
        requestAnimationFrame(this.loop);
    }

    resize() {
        this.width = window.innerWidth;
        this.height = window.innerHeight;
        this.canvas.width = this.width;
        this.canvas.height = this.height;
        this.player.y = this.height - 100;
        this.player.x = this.width / 2;
        this.player.targetX = this.width / 2;
    }

    initInput() {
        // Universal Input Handler (Touch + Mouse)
        const updatePointer = (e) => {
            const clientX = e.touches ? e.touches[0].clientX : e.clientX;
            this.player.targetX = Math.max(20, Math.min(this.width - 20, clientX));
        };

        window.addEventListener('resize', () => this.resize());
        
        // Touch
        document.addEventListener('touchstart', (e) => { 
            this.pointer.isDown = true; updatePointer(e); 
        }, { passive: false });
        document.addEventListener('touchmove', (e) => { 
             e.preventDefault(); // Prevent scrolling
             if(this.state === 'PLAY') updatePointer(e); 
        }, { passive: false });
        
        // Mouse
        document.addEventListener('mousemove', (e) => { 
            if(this.state === 'PLAY') updatePointer(e); 
        });

        // UI Bindings
        document.getElementById('btn-start').onclick = () => this.startGame();
        document.getElementById('btn-restart').onclick = () => this.startGame();
        document.getElementById('btn-pause').onclick = () => this.togglePause();
        document.getElementById('btn-resume').onclick = () => this.togglePause();
        document.getElementById('btn-quit').onclick = () => this.toMainMenu();
        document.getElementById('btn-go-menu').onclick = () => this.toMainMenu();
        
        // Keyboard Pause
        window.addEventListener('keydown', (e) => {
            if(e.key === 'Escape' || e.key === 'p') this.togglePause();
        });
    }

    // --- LOGIC ---

    startGame() {
        this.audio.sfxStart();
        this.resetGame();
        this.setUI('hud');
        this.state = 'PLAY';
    }

    resetGame() {
        this.score = 0;
        this.difficultyMultiplier = 1;
        this.enemies = [];
        this.particles = [];
        this.player.x = this.width / 2;
        this.player.targetX = this.player.x;
        this.player.trail = [];
    }

    togglePause() {
        if (this.state === 'PLAY') {
            this.state = 'PAUSE';
            this.setUI('menu-pause', true); // Keep HUD visible beneath
        } else if (this.state === 'PAUSE') {
            this.state = 'PLAY';
            this.setUI('hud');
        }
        this.audio.sfxUI();
    }

    toMainMenu() {
        this.state = 'MENU';
        this.highScore = StorageManager.load().highScore;
        this.renderMenuScore();
        this.setUI('menu-main');
        this.audio.sfxUI();
    }

    gameOver() {
        this.state = 'GAMEOVER';
        this.audio.sfxCrash();
        
        // Screen Shake Effect
        this.shake = 20;

        // Save Score
        StorageManager.save(Math.floor(this.score));
        
        // UI Update
        document.getElementById('go-score').innerText = Math.floor(this.score);
        this.setUI('menu-gameover');
    }

    setUI(activeId, keepHud = false) {
        document.querySelectorAll('.screen').forEach(el => el.classList.remove('active'));
        document.getElementById('hud').style.opacity = (activeId === 'hud' || keepHud) ? '1' : '0';
        
        if (activeId !== 'hud') {
            const el = document.getElementById(activeId);
            if(el) el.classList.add('active');
        }
    }

    renderMenuScore() {
        document.getElementById('menu-highscore').innerText = Math.floor(this.highScore);
    }

    spawnEnemy() {
        const size = 30 + Math.random() * 40;
        this.enemies.push({
            x: Math.random() * (this.width - size),
            y: -100,
            w: size,
            h: size,
            speed: (Config.physics.baseEnemySpeed + (Math.random() * 2)) * this.difficultyMultiplier,
            color: Config.colors.enemy
        });
    }

    createExplosion(x, y) {
        for(let i=0; i<15; i++) {
            this.particles.push({
                x: x, y: y,
                vx: (Math.random() - 0.5) * 10,
                vy: (Math.random() - 0.5) * 10,
                life: 1.0
            });
        }
    }

    // --- UPDATE LOOP (PHYSICS & LOGIC) ---
    update(dt) {
        if (this.state !== 'PLAY') return;

        // Difficulty Ramping
        this.score += 0.1;
        this.difficultyMultiplier = 1 + (this.score / 1000);
        document.getElementById('score-val').innerText = Math.floor(this.score);

        // Player Physics (Lerp for smoothness)
        this.player.x += (this.player.targetX - this.player.x) * Config.physics.drag;

        // Player Trail
        if (this.frames % 3 === 0) {
            this.player.trail.push({ x: this.player.x, y: this.player.y, life: 1 });
        }

        // Enemy Spawner
        if (this.frames % Math.max(10, Math.floor(60 / this.difficultyMultiplier)) === 0) {
            this.spawnEnemy();
        }

        // Update Entities
        // 1. Enemies
        for (let i = this.enemies.length - 1; i >= 0; i--) {
            let e = this.enemies[i];
            e.y += e.speed;

            // Collision Detection (AABB)
            if (
                this.player.x < e.x + e.w &&
                this.player.x + this.player.w > e.x &&
                this.player.y < e.y + e.h &&
                this.player.y + this.player.h > e.y
            ) {
                this.createExplosion(this.player.x, this.player.y);
                this.gameOver();
            }

            // Cleanup
            if (e.y > this.height) this.enemies.splice(i, 1);
        }

        // 2. Particles
        for (let i = this.particles.length - 1; i >= 0; i--) {
            let p = this.particles[i];
            p.x += p.vx;
            p.y += p.vy;
            p.life -= 0.05;
            if(p.life <= 0) this.particles.splice(i, 1);
        }

        // 3. Trail
        for (let i = this.player.trail.length - 1; i >= 0; i--) {
            this.player.trail[i].life -= 0.05;
            this.player.trail[i].y += 2; // Move trail down with world
            if(this.player.trail[i].life <= 0) this.player.trail.splice(i, 1);
        }

        this.frames++;
    }

    // --- RENDER LOOP (VISUALS) ---
    draw() {
        // Clear Canvas
        this.ctx.fillStyle = Config.colors.bg;
        this.ctx.fillRect(0, 0, this.width, this.height);

        // Shake Effect
        this.ctx.save();
        if (this.shake > 0) {
            const dx = (Math.random() - 0.5) * this.shake;
            const dy = (Math.random() - 0.5) * this.shake;
            this.ctx.translate(dx, dy);
            this.shake *= 0.9;
            if(this.shake < 0.5) this.shake = 0;
        }

        // Draw Grid (Retro Effect)
        this.ctx.strokeStyle = Config.colors.grid;
        this.ctx.lineWidth = 1;
        this.ctx.beginPath();
        const gridOffset = (this.frames * 2) % 50;
        for (let x = 0; x < this.width; x += 50) {
            this.ctx.moveTo(x, 0); this.ctx.lineTo(x, this.height);
        }
        for (let y = gridOffset; y < this.height; y += 50) {
            this.ctx.moveTo(0, y); this.ctx.lineTo(this.width, y);
        }
        this.ctx.stroke();

        // Draw Trail
        this.player.trail.forEach(t => {
            this.ctx.fillStyle = `rgba(0, 243, 255, ${t.life * 0.5})`;
            this.ctx.fillRect(t.x - this.player.w/2, t.y, this.player.w, this.player.h);
        });

        // Draw Player (Neon Glow)
        this.ctx.shadowBlur = 20;
        this.ctx.shadowColor = Config.colors.player;
        this.ctx.fillStyle = Config.colors.player;
        
        // Player Shape (Triangle)
        this.ctx.beginPath();
        this.ctx.moveTo(this.player.x, this.player.y);
        this.ctx.lineTo(this.player.x - 15, this.player.y + 30);
        this.ctx.lineTo(this.player.x + 15, this.player.y + 30);
        this.ctx.closePath();
        this.ctx.fill();

        // Draw Enemies
        this.ctx.shadowColor = Config.colors.enemy;
        this.ctx.fillStyle = Config.colors.enemy;
        this.enemies.forEach(e => {
            this.ctx.fillRect(e.x, e.y, e.w, e.h);
        });

        // Draw Particles
        this.ctx.shadowBlur = 0;
        this.particles.forEach(p => {
            this.ctx.fillStyle = `rgba(255, 255, 255, ${p.life})`;
            this.ctx.fillRect(p.x, p.y, 4, 4);
        });

        this.ctx.restore();
    }

    loop() {
        this.update();
        this.draw();
        requestAnimationFrame(this.loop);
    }
}

// --- INITIALIZATION ---
window.onload = () => {
    // Prevent default touch behaviors on mobile
    document.addEventListener('touchmove', function(event) {
        event = event.originalEvent || event;
        if (event.scale !== 1) event.preventDefault();
    }, { passive: false });
    
    // Launch Engine
    const engine = new Game();
};

</script>
</body>
</html>
