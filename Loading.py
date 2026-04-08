
import sys
import time
import threading
import itertools

# Import colors from config
try:
    from config import RED, GREEN, YELLOW, BLUE, CYAN, MAGENTA, BOLD, RESET
except ImportError:
    # Fallback colors if config not available
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'


class LoadingAnimation:
    """Thread-safe loading animation manager."""
    
    def __init__(self):
        self._running = False
        self._thread = None
    
    def start(self, style="cyber", message="Processing"):
        """Start a loading animation in a background thread."""
        self._running = True
        self._thread = threading.Thread(target=self._animate, args=(style, message), daemon=True)
        self._thread.start()
    
    def stop(self, complete_msg="Done!", success=True):
        """Stop the loading animation."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=1)
        
        symbol = f"{GREEN}✓{RESET}" if success else f"{RED}✗{RESET}"
        sys.stdout.write(f'\r{symbol} {complete_msg}' + ' ' * 40 + '\n')
        sys.stdout.flush()
    
    def _animate(self, style, message):
        """Run the animation loop."""
        animations = {
            "cyber": self._cyber_spinner,
            "matrix": self._matrix_loader,
            "pulse": self._pulse_loader,
            "blocks": self._block_loader,
            "dots": self._dots_loader,
            "hack": self._hacker_loader,
            "wave": self._wave_loader,
        }
        
        anim_func = animations.get(style, self._cyber_spinner)
        anim_func(message)
    
    def _cyber_spinner(self, message):
        """Cyberpunk-style spinner."""
        frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        colors = [RED, YELLOW, GREEN, CYAN, BLUE, MAGENTA]
        i = 0
        while self._running:
            color = colors[i % len(colors)]
            frame = frames[i % len(frames)]
            sys.stdout.write(f'\r{color}{frame}{RESET} {message}...')
            sys.stdout.flush()
            time.sleep(0.08)
            i += 1
    
    def _matrix_loader(self, message):
        """Matrix-style loading with random characters."""
        chars = "01"
        width = 20
        while self._running:
            import random
            bar = ''.join(random.choice(chars) for _ in range(width))
            sys.stdout.write(f'\r{GREEN}[{bar}]{RESET} {message}...')
            sys.stdout.flush()
            time.sleep(0.1)
    
    def _pulse_loader(self, message):
        """Pulsing bar animation."""
        frames = [
            '█░░░░░░░░░',
            '██░░░░░░░░',
            '███░░░░░░░',
            '████░░░░░░',
            '█████░░░░░',
            '██████░░░░',
            '███████░░░',
            '████████░░',
            '█████████░',
            '██████████',
            '█████████░',
            '████████░░',
            '███████░░░',
            '██████░░░░',
            '█████░░░░░',
            '████░░░░░░',
            '███░░░░░░░',
            '██░░░░░░░░',
            '█░░░░░░░░░',
        ]
        i = 0
        while self._running:
            sys.stdout.write(f'\r{CYAN}[{frames[i % len(frames)]}]{RESET} {message}...')
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
    
    def _block_loader(self, message):
        """Block-based progress animation."""
        blocks = ['▏', '▎', '▍', '▌', '▋', '▊', '▉', '█']
        width = 10
        pos = 0
        direction = 1
        while self._running:
            bar = '░' * width
            bar = bar[:pos] + f'{YELLOW}█{RESET}' + bar[pos+1:]
            sys.stdout.write(f'\r[{bar}] {message}...')
            sys.stdout.flush()
            pos += direction
            if pos >= width - 1 or pos <= 0:
                direction *= -1
            time.sleep(0.1)
    
    def _dots_loader(self, message):
        """Bouncing dots animation."""
        frames = [
            '●○○○○',
            '○●○○○',
            '○○●○○',
            '○○○●○',
            '○○○○●',
            '○○○●○',
            '○○●○○',
            '○●○○○',
        ]
        colors = [RED, YELLOW, GREEN, CYAN, BLUE]
        i = 0
        while self._running:
            color = colors[i % len(colors)]
            sys.stdout.write(f'\r{color}{frames[i % len(frames)]}{RESET} {message}...')
            sys.stdout.flush()
            time.sleep(0.15)
            i += 1
    
    def _hacker_loader(self, message):
        """Hacker-style loading with brackets."""
        frames = [
            '[■□□□□□□□□□]',
            '[■■□□□□□□□□]',
            '[■■■□□□□□□□]',
            '[■■■■□□□□□□]',
            '[■■■■■□□□□□]',
            '[■■■■■■□□□□]',
            '[■■■■■■■□□□]',
            '[■■■■■■■■□□]',
            '[■■■■■■■■■□]',
            '[■■■■■■■■■■]',
        ]
        i = 0
        while self._running:
            pct = (i % 10 + 1) * 10
            sys.stdout.write(f'\r{RED}{frames[i % len(frames)]}{RESET} {GREEN}{pct}%{RESET} {message}...')
            sys.stdout.flush()
            time.sleep(0.2)
            i += 1
    
    def _wave_loader(self, message):
        """Wave animation."""
        frames = ['▁▂▃▄▅▆▇█▇▆▅▄▃▂▁', '▂▃▄▅▆▇█▇▆▅▄▃▂▁▁', '▃▄▅▆▇█▇▆▅▄▃▂▁▁▂',
                  '▄▅▆▇█▇▆▅▄▃▂▁▁▂▃', '▅▆▇█▇▆▅▄▃▂▁▁▂▃▄', '▆▇█▇▆▅▄▃▂▁▁▂▃▄▅',
                  '▇█▇▆▅▄▃▂▁▁▂▃▄▅▆', '█▇▆▅▄▃▂▁▁▂▃▄▅▆▇']
        i = 0
        while self._running:
            sys.stdout.write(f'\r{CYAN}{frames[i % len(frames)]}{RESET} {message}...')
            sys.stdout.flush()
            time.sleep(0.12)
            i += 1


# Global loader instance for easy use
_loader = LoadingAnimation()


def start_loading(message="Processing", style="cyber"):
    """Start a cool loading animation.
    
    Styles: cyber, matrix, pulse, blocks, dots, hack, wave
    """
    _loader.start(style=style, message=message)


def stop_loading(complete_msg="Done!", success=True):
    """Stop the loading animation."""
    _loader.stop(complete_msg, success)


def with_loading(message="Processing", style="cyber", complete_msg="Done!"):
    """Decorator to add loading animation to a function."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_loading(message, style)
            try:
                result = func(*args, **kwargs)
                stop_loading(complete_msg)
                return result
            except Exception as e:
                stop_loading(f"Error: {e}")
                raise
        return wrapper
    return decorator


def quick_loading(message="Loading", duration=2, style="cyber"):
    """Show a loading animation for a fixed duration."""
    start_loading(message, style)
    time.sleep(duration)
    stop_loading()


# Simple non-threaded animations for quick use
def simple_dots(message="Loading", count=3):
    """Simple dots animation (blocking)."""
    print(f"{message}", end="", flush=True)
    for _ in range(count):
        for _ in range(3):
            print(".", end="", flush=True)
            time.sleep(0.3)
        print("\b\b\b   \b\b\b", end="", flush=True)
    print(" ✓")


def progress_bar(current, total, message="Progress", width=30):
    """Display a progress bar (call repeatedly to update)."""
    percent = current / total
    filled = int(width * percent)
    bar = '█' * filled + '░' * (width - filled)
    sys.stdout.write(f'\r{CYAN}[{bar}]{RESET} {GREEN}{percent*100:.1f}%{RESET} {message}')
    sys.stdout.flush()
    if current >= total:
        print()
