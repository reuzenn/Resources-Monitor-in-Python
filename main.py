import glfw
import OpenGL.GL as gl
import imgui
from imgui.integrations.glfw import GlfwRenderer
import sys

# Oluşturduğumuz modülleri içe aktarıyoruz
import cpu
import ram

def main():
    if not glfw.init():
        sys.exit(1)

    # Pencere ayarları
    glfw.window_hint(glfw.DECORATED, False)
    glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, True)
    glfw.window_hint(glfw.FLOATING, True)
    glfw.window_hint(glfw.MOUSE_PASSTHROUGH, True)

    # Çözünürlük ayarları
    widget_w, widget_h = 300, 100 
    
    window = glfw.create_window(widget_w, widget_h, "SystemMonitor", None, None)
    glfw.make_context_current(window)

    imgui.create_context()
    impl = GlfwRenderer(window)

    # Başlangıç değerleri
    cpu_val = 0.0
    ram_val = 0.0
    mem_used = 0.0
    mem_total = 0.0
    
    last_update = 0.0

    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()

        # Her 1 saniyede bir güncelle
        if glfw.get_time() - last_update > 1.0:
            # Verileri kendi modüllerinden çekiyoruz
            cpu_val = cpu.get_cpu_usage()
            ram_val, mem_used, mem_total = ram.get_ram_info()
            
            last_update = glfw.get_time()

        imgui.new_frame()

        # Pencereyi sabitle
        imgui.set_next_window_position(20, 20)
        imgui.set_next_window_size(widget_w, widget_h)
        
        imgui.begin("Overlay", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_BACKGROUND | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_INPUTS)

        # Yazıları bas
        imgui.text(f"CPU: %{cpu_val}")
        imgui.text(f"RAM: %{ram_val} ({mem_used}/{mem_total} GB)")

        imgui.end()

        # Render
        gl.glClearColor(0, 0, 0, 0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        imgui.render()
        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)

    impl.shutdown()
    glfw.terminate()

if __name__ == "__main__":
    main()