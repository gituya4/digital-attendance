import os
import socket
from app import create_app

app = create_app()

def get_local_ip():
    """Get the local IP address of the machine"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

if __name__ == '__main__':
    debug = os.getenv('FLASK_DEBUG', 'False') == 'True'
    
    # Check if SSL certificates exist
    ssl_context = None
    if os.path.exists('cert.pem') and os.path.exists('key.pem'):
        ssl_context = ('cert.pem', 'key.pem')
        print("\n🔒 HTTPS enabled with SSL certificates")
        print(f"\n📱 Access from your phone using:")
        local_ip = get_local_ip()
        print(f"   https://{local_ip}:5000")
        print(f"   https://localhost:5000")
        print(f"\n⚠️  Your browser will show a security warning")
        print(f"   Click 'Advanced' -> 'Proceed to {local_ip} (unsafe)' to continue\n")
    else:
        print("\n⚠️  SSL certificates not found - running in HTTP mode")
        print("   Camera access may not work without HTTPS")
        print("   Run 'openssl' commands to generate certificates\n")
    
    app.run(debug=debug, host='0.0.0.0', port=5000, ssl_context=ssl_context)
