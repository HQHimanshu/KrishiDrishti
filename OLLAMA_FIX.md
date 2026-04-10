# 🤖 Fix Ollama Memory Issue - KrishiDrishti

## ❌ Your Current Problem

```
model request too large for system
requested="10.1 GiB" 
available="5.6 GiB"
total="15.7 GiB" 
free="2.7 GiB"
```

**qwen2.5vl:3b** requires **10.1 GB RAM** but you only have **5.6 GB free**.

---

## ✅ SOLUTIONS (Choose One)

### Option 1: Free Up RAM (Easiest) ⭐⭐⭐

**Close these programs to free memory:**
1. **Browser tabs** - Each tab uses 200-500 MB
   - Close all except localhost:5173
2. **VS Code extensions** - Can use 1-2 GB
3. **Background apps** - Discord, Spotify, etc.
4. **Docker** (if running) - Uses 2-4 GB

**After closing apps, restart Ollama:**
```bash
# Stop Ollama (from task manager - end ollama.exe process)
# Then restart:
ollama serve
```

**Check if it works:**
```bash
curl http://localhost:11434/api/generate -d "{\"model\":\"qwen2.5vl:3b\",\"prompt\":\"Hello\",\"stream\":false}"
```

---

### Option 2: Use Smaller Model (Guaranteed to Work) ⭐⭐

**Use qwen2.5:1.5b** instead (needs only ~3 GB):

```bash
# Pull smaller model
ollama pull qwen2.5:1.5b

# Update .env
OLLAMA_MODEL=qwen2.5:1.5b

# Restart backend
```

**Trade-off**: Less accurate than 3b, but will work on your system

---

### Option 3: Run Ollama Without Loading Other Apps

**Best practice for AI development:**
1. **Restart your computer**
2. **Before opening anything else:**
   - Start Ollama: `ollama serve`
   - Start Backend
   - Start Frontend
   - Open browser
3. **Don't open** heavy apps (games, video editors, etc.)

This gives Ollama maximum available RAM.

---

## 🎯 RECOMMENDED APPROACH

**For your 16 GB system:**

1. **Close ALL unnecessary programs**
2. **Restart Ollama**
3. **Try qwen2.5vl:3b again**

**If still fails:**
- Switch to `qwen2.5:1.5b` (works guaranteed)
- Still gives you AI chat, just slightly less accurate

---

## 📝 How to Switch Models

1. **Update `.env`:**
```env
OLLAMA_MODEL=qwen2.5:1.5b
```

2. **Restart backend:**
```bash
# Kill current backend
taskkill /F /IM python.exe /T

# Start again
cd D:\Himanshu_Project\KrishiDrishti\backend
venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

3. **Test:**
```bash
curl http://localhost:11434/api/generate -d "{\"model\":\"qwen2.5:1.5b\",\"prompt\":\"Hello\",\"stream\":false}"
```

---

## 💡 Memory Usage Reference

| Model | RAM Required | Quality |
|-------|--------------|---------|
| qwen2.5vl:3b | 10 GB | Good (current, not loading) |
| qwen2.5:1.5b | 3 GB | Decent (recommended for you) |
| qwen2.5:0.5b | 1.5 GB | Basic (works on any system) |

---

## ✅ Verify It Works

```bash
# Test Ollama
curl http://localhost:11434/api/generate ^
  -d "{\"model\":\"qwen2.5:1.5b\",\"prompt\":\"What is farming?\",\"stream\":false}"

# Should return JSON with "response" field
```
