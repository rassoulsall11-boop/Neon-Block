"""
TRIAS OS - ULTRA IA MAX FUSION (Enterprise + Auto-Apprentissage)
Architecture: MVC / MVVM Inspired
Concurrency: ThreadPoolExecutor / Async tasks
Storage: Atomic JSON + Fernet Encryption
"""

import os, json, time, socket, logging, threading
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Callable, Any
from concurrent.futures import ThreadPoolExecutor

import customtkinter as ctk
from tkinter import Canvas
from PIL import Image, ImageTk
from cryptography.fernet import Fernet
from openai import OpenAI

# ================= CONFIG & LOGGING =================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("TRIAS_CORE")

@dataclass
class AppConfig:
    BASE_DIR: Path = Path.home() / "Desktop" / "TRIAS_PROJECT"
    LOGO_PATH: Path = field(init=False)
    VAULT_PATH: Path = field(init=False)
    MEMORY_PATH: Path = field(init=False)
    KEY_PATH: Path = field(init=False)
    API_KEY: str = os.environ.get("OPENAI_API_KEY", "TA_CLE_API_ICI")
    
    def __post_init__(self):
        self.BASE_DIR.mkdir(parents=True, exist_ok=True)
        self.LOGO_PATH = self.BASE_DIR / "logo.png"
        self.VAULT_PATH = self.BASE_DIR / "vault.json"
        self.MEMORY_PATH = self.BASE_DIR / "ai_memory.json"
        self.KEY_PATH = self.BASE_DIR / "key.key"

CONFIG = AppConfig()

# ================= CRYPTO SERVICE =================
class CryptoService:
    def __init__(self, key_path: Path):
        self.key_path = key_path
        self._fernet: Fernet = None
        self._initialize_key()

    def _initialize_key(self):
        if not self.key_path.exists():
            key = Fernet.generate_key()
            self.key_path.write_bytes(key)
            os.chmod(str(self.key_path), 0o600)
        self._fernet = Fernet(self.key_path.read_bytes())

    def encrypt(self, data: str) -> str:
        return self._fernet.encrypt(data.encode()).decode()

    def decrypt(self, token: str) -> str:
        try:
            return self._fernet.decrypt(token.encode()).decode()
        except: return "[DECRYPTION_ERROR]"

# ================= STORAGE SERVICE =================
class StorageService:
    _lock = threading.Lock()
    @classmethod
    def load(cls, path: Path, default: Any = None) -> Any:
        with cls._lock:
            if not path.exists(): return default if default is not None else []
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except: return default if default is not None else []

    @classmethod
    def save(cls, path: Path, data: Any):
        with cls._lock:
            temp = path.with_suffix('.tmp')
            temp.write_text(json.dumps(data, indent=4, ensure_ascii=False), encoding="utf-8")
            temp.replace(path)

# ================= AI SERVICE =================
class AIService:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.history: List[Dict] = StorageService.load(CONFIG.MEMORY_PATH, [])
        self.patterns: Dict[str,int] = {}
        self.summary_cache: str = ""
        self.executor = ThreadPoolExecutor(max_workers=2)
        self.analyze_patterns()

    def analyze_patterns(self):
        freq={}
        for h in self.history:
            q=h.get('q','').lower()
            freq[q]=freq.get(q,0)+1
        self.patterns=dict(sorted(freq.items(), key=lambda x:x[1], reverse=True))

    def ping_status(self) -> bool:
        try: self.client.models.list(timeout=2.0); return True
        except: return False

    def compress_history(self) -> str:
        if not self.history: return ""
        conv="\n".join([f"Q:{h['q']} A:{h['r']}" for h in self.history[-50:]])
        prompt=f"Résume en phrases clés:\n{conv}"
        try:
            resp=self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role":"user","content":prompt}]
            )
            return resp.choices[0].message.content
        except: return ""

    def query_async(self, question: str, callback: Callable[[str], None]):
        def task():
            try:
                messages=[{"role":"system","content":"Tu es TRIAS, IA ultra intelligente, légale et contextuelle."}]
                if self.summary_cache: messages.append({"role":"system","content":f"Contexte: {self.summary_cache}"})
                if self.patterns:
                    top=[p for p in list(self.patterns.keys())[:5]]
                    messages.append({"role":"system","content":f"Patterns: {', '.join(top)}"})
                messages.append({"role":"user","content":question})
                resp=self.client.chat.completions.create(model="gpt-4o-mini", messages=messages, timeout=15)
                answer=resp.choices[0].message.content or "..."
            except Exception as e:
                answer=f"[SYSTEM EXCEPTION] {e}"
            self.history.append({"q":question,"r":answer,"t":time.time()})
            StorageService.save(CONFIG.MEMORY_PATH,self.history)
            self.analyze_patterns()
            callback(answer)
        self.executor.submit(task)

# ================= NETWORK SCANNER =================
class NetworkScanner:
    def __init__(self): self.executor=ThreadPoolExecutor(max_workers=200)
    def scan_ports(self, ip:str, callback:Callable[[int],None], done_callback:Callable[[],None]):
        def scan(port):
            with socket.socket() as s:
                s.settimeout(0.2)
                if s.connect_ex((ip,port))==0: callback(port)
        def runner():
            futures=[self.executor.submit(scan,p) for p in range(1,1025)]
            for _ in futures: pass
            done_callback()
        threading.Thread(target=runner,daemon=True).start()

# ================= UI COMPONENTS =================
class TriasSplash(ctk.CTkToplevel):
    def __init__(self, master, on_complete:Callable):
        super().__init__(master)
        self.on_complete=on_complete; self.overrideredirect(True); self.geometry("600x400"); self.configure(fg_color="black")
        self._center(); self._build(); self.anim=0; self.after(10,self._animate)

    def _center(self):
        self.update_idletasks()
        x=(self.winfo_screenwidth()//2)-300; y=(self.winfo_screenheight()//2)-200
        self.geometry(f"+{x}+{y}")

    def _build(self):
        self.canvas=Canvas(self,bg="black",highlightthickness=0); self.canvas.pack(fill="both",expand=True)
        try:
            img=Image.open(CONFIG.LOGO_PATH).resize((180,180)) if CONFIG.LOGO_PATH.exists() else Image.new('RGB',(180,180),'#0044ff')
            self.tk_logo=ImageTk.PhotoImage(img)
            self.l_img=self.canvas.create_image(-100,200,image=self.tk_logo)
            self.r_img=self.canvas.create_image(700,200,image=self.tk_logo)
        except Exception as e: logger.error(f"Splash image load failed: {e}")

    def _animate(self):
        if self.anim<80: self.canvas.move(self.l_img,5,0); self.canvas.move(self.r_img,-5,0); self.anim+=1; self.after(10,self._animate)
        else: self.destroy(); self.on_complete()

class AITab(ctk.CTkFrame):
    def __init__(self, master, ai:AIService):
        super().__init__(master); self.ai=ai; self._build(); self._load_history(); self._start_ping()

    def _build(self):
        self.status=Canvas(self,width=20,height=20,bg="black",highlightthickness=0); self.status.pack(padx=10,pady=5,anchor="ne")
        self.indicator=self.status.create_oval(2,2,18,18,fill="red")
        self.chat=ctk.CTkTextbox(self,fg_color="#0a0a0a",text_color="#00ffcc",font=("Cascadia Code",13)); self.chat.pack(fill="both",expand=True,padx=10,pady=(0,10)); self.chat.configure(state="disabled")
        self.entry=ctk.CTkEntry(self,placeholder_text="TRIAS en attente...",font=("Cascadia Code",13)); self.entry.pack(fill="x",padx=10,pady=10); self.entry.bind("<Return>",self._handle_input)

    def _load_history(self):
        self.chat.configure(state="normal")
        for h in self.ai.history[-15:]: self.chat.insert("end",f"\n[USER] {h['q']}\n[TRIAS] {h['r']}\n")
        self.chat.see("end"); self.chat.configure(state="disabled")

    def _start_ping(self):
        def pinger():
            while True:
                is_up=self.ai.ping_status(); color="#00ff00" if is_up else "#ff0000"
                if self.winfo_exists(): self.after(0,lambda: self.status.itemconfig(self.indicator,fill=color))
                time.sleep(30)
        threading.Thread(target=pinger,daemon=True).start()

    def _handle_input(self,event=None):
        q=self.entry.get().strip(); 
        if not q: return; self.entry.delete(0,"end"); self.entry.configure(state="disabled")
        self.chat.configure(state="normal"); self.chat.insert("end",f"\n[USER] {q}\n"); self.chat.see("end"); self.chat.configure(state="disabled")
        self.ai.query_async(q,self._on_response)

    def _on_response(self,text:str):
        if not self.winfo_exists(): return
        self.chat.configure(state="normal"); self.chat.insert("end","[TRIAS] "); self._typewriter(text,0)

    def _typewriter(self,text,index):
        if not self.winfo_exists(): return
        if index<len(text): self.chat.insert("end",text[index]); self.chat.see("end"); self.after(5,lambda:self._typewriter(text,index+1))
        else: self.chat.insert("end","\n"); self.chat.see("end"); self.chat.configure(state="disabled"); self.entry.configure(state="normal"); self.entry.focus()

class ScannerTab(ctk.CTkFrame):
    def __init__(self, master, scanner:NetworkScanner):
        super().__init__(master); self.scanner=scanner; self._build()

    def _build(self):
        self.ip=ctk.CTkEntry(self,placeholder_text="Cible (192.168.x.x ou 127.0.0.1)"); self.ip.pack(pady=20,padx=20,fill="x")
        self.btn=ctk.CTkButton(self,text="SCAN",command=self._start_scan,fg_color="#550000",hover_color="#ff0000"); self.btn.pack(pady=5)
        self.console=ctk.CTkTextbox(self,fg_color="#0a0a0a",text_color="#ff5555",font=("Courier",13)); self.console.pack(fill="both",expand=True,padx=20,pady=20)

    def _start_scan(self):
        target=self.ip.get().strip()
        if not target.startswith("192.168") and target!="127.0.0.1": self._log("RESTRICTED: Local scan only.\n"); return
        self.btn.configure(state="disabled"); self.console.delete("1.0","end"); self._log(f"INITIALIZING SCAN ON {target}...\n")
        self.scanner.scan_ports(target,self._on_port,self._on_done)

    def _on_port(self,port): self.after(0,lambda:self._log(f"-> OPEN PORT: {port}\n"))
    def _on_done(self): self.after(0,lambda:self._log("SCAN COMPLETE\n")); self.after(0,lambda:self.btn.configure(state="normal"))
    def _log(self,text): self.console.insert("end",text); self.console.see("end")

class VaultTab(ctk.CTkFrame):
    def __init__(self, master, crypto:CryptoService):
        super().__init__(master); self.crypto=crypto; self._build(); self._load()

    def _build(self):
        header=ctk.CTkFrame(self,fg_color="transparent"); header.pack(fill="x",padx=20,pady=20)
        self.name=ctk.CTkEntry(header,placeholder_text="IDENTIFIANT"); self.name.pack(side="left",fill="x",expand=True,padx=(0,5))
        self.pwd=ctk.CTkEntry(header,placeholder_text="CLE D'ACCES",show="*"); self.pwd.pack(side="left",fill="x",expand=True,padx=5)
        ctk.CTkButton(header,text="ENCRYPTER",command=self._save).pack(side="left",padx=(5,0))
        self.console=ctk.CTkTextbox(self,fg_color="#0a0a0a",text_color="#aaaaaa",font=("Courier",13)); self.console.pack(fill="both",expand=True,padx=20,pady=(0,20)); self.console.configure(state="disabled")

    def _save(self):
        name=self.name.get().strip(); pwd=self.pwd.get().strip(); 
        if not name or not pwd: return
        data=StorageService.load(CONFIG.VAULT_PATH,[]); data.append({"name":name,"pass":self.crypto.encrypt(pwd)})
        StorageService.save(CONFIG.VAULT_PATH,data)
        self.name.delete(0,"end"); self.pwd.delete(0,"end"); self._log(f"[LOCKED] {name} encrypted.\n")

    def _load(self):
        data=StorageService.load(CONFIG.VAULT_PATH,[]); self._log(f"[SYSTEM] {len(data)} entries in vault.\n")
    def _log(self,text): self.console.configure(state="normal"); self.console.insert("end",text); self.console.see("end"); self.console.configure(state="disabled")

# ================= MAIN APPLICATION =================
class TriasOS(ctk.CTk):
    def __init__(self):
        super().__init__(); ctk.set_appearance_mode("dark"); self.withdraw()
        self.crypto=CryptoService(CONFIG.KEY_PATH)
        self.ai_service=AIService(CONFIG.API_KEY)
        self.scanner_service=NetworkScanner()
        TriasSplash(self,on_complete=self.initialize)

    def initialize(self):
        self.deiconify(); self.title("TRIAS OS – FUSION ENTERPRISE"); self.geometry("1200x800"); self.minsize(800,600)
        self.sidebar=ctk.CTkFrame(self,width=220,corner_radius=0); self.sidebar.pack(side="left",fill="y")
        self.main_container=ctk.CTkFrame(self,corner_radius=0,fg_color="black"); self.main_container.pack(side="right",fill="both",expand=True)
        self.views={
            "AI_CORE":AITab(self.main_container,self.ai_service),
            "NET_SCAN":ScannerTab(self.main_container,self.scanner_service),
            "SYS_VAULT":VaultTab(self.main_container,self.crypto)
        }
        ctk.CTkLabel(self.sidebar,text="TRIAS OS",font=("Arial Black",20)).pack(pady=20)
        for name in self.views.keys(): ctk.CTkButton(self.sidebar,text=name.replace("_"," "),font=("Arial",14,"bold"),height=40,command=lambda n=name:self.switch_view(n)).pack(fill="x",padx=10,pady=5)
        self.switch_view("AI_CORE")

    def switch_view(self,name:str):
        for v in self.views.values(): v.pack_forget()
        self.views[name].pack(fill="both",expand=True)

# ================= ENTRY POINT =================
if __name__=="__main__":
    try:
        app=TriasOS()
        app.mainloop()
    except KeyboardInterrupt:
        logger.info("Shutdown requested."); os._exit(0)
