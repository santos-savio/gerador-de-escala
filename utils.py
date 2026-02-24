import bcrypt
import secrets
import string
import os
from slugify import slugify
from playwright.sync_api import sync_playwright

# Configuração
OG_IMAGES_DIR = os.path.join('public', 'ogImagesEscalas')

def hash_password(password):
    """Gera hash da senha usando bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def check_password(password, password_hash):
    """Verifica se a senha corresponde ao hash"""
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def ensure_og_images_dir():
    """Garante que o diretório de imagens OG existe"""
    if not os.path.exists(OG_IMAGES_DIR):
        os.makedirs(OG_IMAGES_DIR, exist_ok=True)

def generate_og_image(html_content, slug):
    """
    Gera uma imagem OG a partir do HTML da escala.
    Retorna o caminho relativo da imagem gerada.
    """
    ensure_og_images_dir()
    
    output_path = os.path.join(OG_IMAGES_DIR, f"{slug}.png")
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1200, 'height': 630})
        
        # Carregar o HTML
        page.set_content(html_content)
        
        # Aguardar carregamento de imagens e fonts
        page.wait_for_load_state('networkidle')
        
        # Tirar screenshot
        page.screenshot(path=output_path, full_page=False)
        
        browser.close()
    
    # Retornar caminho relativo para uso nas OG tags
    return f"/ogImagesEscalas/{slug}.png"

def get_og_image_path(slug):
    """Retorna o caminho da imagem OG se ela existir, ou None"""
    image_path = os.path.join(OG_IMAGES_DIR, f"{slug}.png")
    if os.path.exists(image_path):
        return f"/ogImagesEscalas/{slug}.png"
    return None

def generate_unique_slug(length=20):
    """Gera um slug único para URLs de escalas"""
    chars = string.ascii_lowercase + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))
