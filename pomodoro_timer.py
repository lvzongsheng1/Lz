import time
import os
import sys
import threading

FOCUS_TIME = 25 * 60
SHORT_BREAK = 5 * 60
LONG_BREAK = 15 * 60

user_input = None
input_lock = threading.Lock()

def get_user_input():
    global user_input
    while True:
        with input_lock:
            if user_input is not None:
                break
        try:
            if os.name == 'nt':
                import msvcrt
                if msvcrt.kbhit():
                    char = msvcrt.getch().decode().lower()
                    if char == 'q':
                        with input_lock:
                            user_input = 'quit'
            else:
                import select
                if select.select([sys.stdin], [], [], 0.1)[0]:
                    line = sys.stdin.readline().strip().lower()
                    if line in ['q', 'quit']:
                        with input_lock:
                            user_input = 'quit'
        except:
            pass
        time.sleep(0.1)

def format_time(seconds):
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"

def clear_line():
    if os.name == 'nt':
        sys.stdout.write('\r')
    else:
        sys.stdout.write('\r\033[K')

def countdown(duration, mode_name):
    global user_input
    user_input = None
    
    input_thread = threading.Thread(target=get_user_input, daemon=True)
    input_thread.start()
    
    remaining = duration
    while remaining >= 0:
        with input_lock:
            if user_input == 'quit':
                print("\n\n用户已退出程序。")
                sys.exit(0)
        
        time_str = format_time(remaining)
        clear_line()
        sys.stdout.write(f"[{mode_name}] 剩余时间: {time_str}")
        sys.stdout.flush()
        
        if remaining == 0:
            break
        
        time.sleep(1)
        remaining -= 1
    
    print()
    print('\a')

def show_encouragement(mode):
    if mode == "focus":
        print("\n🎉 专注周期完成！干得漂亮！")
    elif mode == "short_break":
        print("\n☕ 短暂休息结束，准备好开始下一轮了吗？")
    elif mode == "long_break":
        print("\n🌟 长休息结束，你完成了一个大周期！")

def main():
    focus_count = 0
    
    print("=" * 40)
    print("🍅 番茄工作法计时器")
    print("=" * 40)
    print("模式选项:")
    print("  1. 开始默认流程 (专注 -> 休息循环)")
    print("  2. 单次专注模式 (25分钟)")
    print("  3. 单次短休息 (5分钟)")
    print("  4. 单次长休息 (15分钟)")
    print("  q. 退出程序")
    print("-" * 40)
    print("提示: 倒计时过程中可随时输入 'q' 退出")
    print("=" * 40)
    
    choice = input("\n请选择操作 (1-4): ").strip().lower()
    
    if choice in ['q', 'quit']:
        print("程序已退出。")
        return
    
    if choice == '1':
        try:
            while True:
                print(f"\n--- 第 {focus_count + 1} 个专注周期 ---")
                countdown(FOCUS_TIME, "专注模式")
                focus_count += 1
                show_encouragement("focus")
                
                if focus_count % 4 == 0:
                    print("\n--- 长休息 ---")
                    countdown(LONG_BREAK, "长休息")
                    show_encouragement("long_break")
                else:
                    print("\n--- 短休息 ---")
                    countdown(SHORT_BREAK, "短休息")
                    show_encouragement("short_break")
                
                cont = input("\n是否继续下一个周期？(y/n, 默认y): ").strip().lower()
                if cont in ['n', 'no', 'q', 'quit']:
                    break
        except KeyboardInterrupt:
            print("\n\n程序已中断。")
        finally:
            print(f"\n本次会话共完成 {focus_count} 个专注周期！")
            print("继续加油！💪")
    
    elif choice == '2':
        print("\n--- 专注模式 ---")
        countdown(FOCUS_TIME, "专注模式")
        focus_count = 1
        show_encouragement("focus")
        print(f"\n本次会话共完成 {focus_count} 个专注周期！")
    
    elif choice == '3':
        print("\n--- 短休息 ---")
        countdown(SHORT_BREAK, "短休息")
        show_encouragement("short_break")
    
    elif choice == '4':
        print("\n--- 长休息 ---")
        countdown(LONG_BREAK, "长休息")
        show_encouragement("long_break")
    
    else:
        print("无效选择，程序退出。")

if __name__ == "__main__":
    main()
