// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tauri::{CustomMenuItem, SystemTray, SystemTrayMenu, SystemTrayMenuItem, Manager};
use std::process::{Command, Child};
use std::sync::{Arc, Mutex};
use serde_json::Value;

// Shared state for the backend process
struct BackendState {
    child: Mutex<Option<Child>>,
}

#[tauri::command]
async fn get_backend_status() -> Result<Value, String> {
    // Proxy call to Python backend over Unix Socket / Named Pipe
    // For this demonstration, we'll simulate the response or use a simple HTTP client 
    // that supports UDS if the platform allows it.
    // In a real implementation, you'd use something like 'hyper' with UDS support.
    
    // Simplified: return mock data if backend isn't reachable
    Ok(serde_json::json!({
        "connected": false,
        "peer": "LocalNode-1",
        "latency": 45.2,
        "stats": {
            "uptime": 3600,
            "upload_speed": 12400,
            "download_speed": 85000,
            "total_sent": 1024000,
            "total_recv": 5048000
        }
    }))
}

#[tauri::command]
async fn connect_vpn(peer_id: i32) -> Result<(), String> {
    println!("Connecting to peer {}", peer_id);
    // Call Python backend
    Ok(())
}

#[tauri::command]
async fn disconnect_vpn() -> Result<(), String> {
    println!("Disconnecting VPN");
    // Call Python backend
    Ok(())
}

#[tauri::command]
async fn get_peers() -> Result<Value, String> {
    Ok(serde_json::json!([
        {"id": 1, "name": "Oracle Cloud Free", "endpoint": "123.123.123.123:51820", "public_key": "abc...", "is_active": false},
        {"id": 2, "name": "Home Server", "endpoint": "home.example.com:51820", "public_key": "xyz...", "is_active": false}
    ]))
}

#[tauri::command]
async fn toggle_killswitch(enabled: bool) -> Result<(), String> {
    println!("Killswitch: {}", enabled);
    Ok(())
}

#[tauri::command]
async fn toggle_dns(enabled: bool, provider: String) -> Result<(), String> {
    println!("DNS: {} via {}", enabled, provider);
    Ok(())
}

fn main() {
    // System Tray Setup
    let quit = CustomMenuItem::new("quit".to_string(), "Quit");
    let hide = CustomMenuItem::new("hide".to_string(), "Hide Dashboard");
    let show = CustomMenuItem::new("show".to_string(), "Show Dashboard");
    let tray_menu = SystemTrayMenu::new()
        .add_item(show)
        .add_item(hide)
        .add_native_item(SystemTrayMenuItem::Separator)
        .add_item(quit);
    let system_tray = SystemTray::new().with_menu(tray_menu);

    tauri::Builder::default()
        .manage(BackendState {
            child: Mutex::new(None),
        })
        .system_tray(system_tray)
        .on_system_tray_event(|app, event| {
            match event {
                tauri::SystemTrayEvent::MenuItemClick { id, .. } => {
                    match id.as_str() {
                        "quit" => {
                            std::process::exit(0);
                        }
                        "show" => {
                            let window = app.get_window("main").unwrap();
                            window.show().unwrap();
                        }
                        "hide" => {
                            let window = app.get_window("main").unwrap();
                            window.hide().unwrap();
                        }
                        _ => {}
                    }
                }
                _ => {}
            }
        })
        .setup(|app| {
            // Start Python Backend
            let backend_path = app.path_resolver().resolve_resource("backend/main.py").unwrap_or_else(|| "src/backend/main.py".into());
            let child = Command::new("python")
                .arg(backend_path)
                .spawn()
                .expect("Failed to start Python backend");
            
            let state = app.state::<BackendState>();
            *state.child.lock().unwrap() = Some(child);
            
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![
            get_backend_status,
            connect_vpn,
            disconnect_vpn,
            get_peers,
            toggle_killswitch,
            toggle_dns
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
