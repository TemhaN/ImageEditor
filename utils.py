import time

def smooth_zoom(ui, step=0):
    if not ui.is_zooming:
        ui.is_zooming = True
        start_time = time.time() * 1000
        start_zoom = ui.zoom_level
        target_zoom = ui.target_zoom
        duration = 200

        def animate():
            try:
                elapsed = (time.time() * 1000) - start_time
                t = min(elapsed / duration, 1.0)
                ui.zoom_level = start_zoom + (target_zoom - start_zoom) * t
                ui.update_image(fast_mode=True)
                if t < 1.0:
                    ui.root.after(10, animate)
                else:
                    ui.zoom_level = target_zoom
                    ui.update_image(fast_mode=False)
                    ui.is_zooming = False
            except Exception as e:
                ui.is_zooming = False

        try:
            ui.root.after(10, animate)
        except Exception as e:
            ui.is_zooming = False