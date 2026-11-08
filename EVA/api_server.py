from modules import task
from modules import notes

from core.speech import (
    take_command,
    speak,
    reset_speech_event,
    get_last_spoken_text,
    speech_started_event,
)

from core import router

from http.server import BaseHTTPRequestHandler, HTTPServer

import json
import threading

import ai_brain

# Import MAIN so all existing command handlers
# are registered with the router.
import MAIN


HOST = "127.0.0.1"
PORT = 5000


class EvaAPIHandler(BaseHTTPRequestHandler):

    def send_json(self, status_code, data):

        response = json.dumps(
            data
        ).encode("utf-8")

        self.send_response(
            status_code
        )

        self.send_header(
            "Content-Type",
            "application/json"
        )

        self.send_header(
            "Content-Length",
            str(len(response))
        )

        self.end_headers()

        self.wfile.write(
            response
        )

    def do_GET(self):

        # ==========================================
        # STARTUP INFORMATION
        # ==========================================

        if self.path == "/startup":

            try:

                note_count = notes.notes_count()

                total_tasks = task.task_count()

                pending_tasks = task.pending_task_count()

                due_tasks = task.get_due_tasks()

                overdue_tasks = task.get_overdue_tasks()

                self.send_json(
                    200,
                    {
                        "status": "online",
                        "note_count": note_count,
                        "total_tasks": total_tasks,
                        "pending_tasks": pending_tasks,
                        "due_tasks": len(due_tasks),
                        "overdue_tasks": len(overdue_tasks),
                    }
                )

            except Exception as e:

                print(
                    "Startup API Error:",
                    e
                )

                self.send_json(
                    500,
                    {
                        "error":
                            "EVA could not load startup information."
                    }
                )

            return

        # ==========================================
        # API STATUS
        # ==========================================

        if self.path == "/":

            self.send_json(
                200,
                {
                    "status": "online",
                    "message": "EVA API is running."
                }
            )

        else:

            self.send_json(
                404,
                {
                    "error": "Endpoint not found."
                }
            )

    def do_POST(self):
        # ==========================================
        # SPEAK
        # ==========================================

        if self.path == "/speak":

            try:

                content_length = int(
                    self.headers.get(
                        "Content-Length",
                        0
                    )
                )

                body = self.rfile.read(
                    content_length
                )

                data = json.loads(
                    body.decode("utf-8")
                )

                message = data.get(
                    "message",
                    ""
                ).strip()

                if not message:

                    self.send_json(
                        400,
                        {
                            "error":
                                "Speech message cannot be empty."
                        }
                    )

                    return

                print(
                    f"[EVA] Startup speech: {message}"
                )

                # Wait until EVA finishes speaking.
                speak(message)

                self.send_json(
                    200,
                    {
                        "spoken": True
                    }
                )

            except json.JSONDecodeError:

                self.send_json(
                    400,
                    {
                        "error": "Invalid JSON."
                    }
                )

            except Exception as e:

                print(
                    "Speech API Error:",
                    e
                )

                self.send_json(
                    500,
                    {
                        "error":
                            "EVA could not speak."
                    }
                )

            return
        # ==========================================
        # LISTEN
        # ==========================================

        if self.path == "/listen":

            try:

                command = take_command()

                self.send_json(
                    200,
                    {
                        "command": command
                    }
                )

            except Exception as e:

                print(
                    "Speech API Error:",
                    e
                )

                self.send_json(
                    500,
                    {
                        "error":
                            "EVA could not listen."
                    }
                )

            return

        # ==========================================
        # CHAT
        # ==========================================

        if self.path != "/chat":

            self.send_json(
                404,
                {
                    "error": "Endpoint not found."
                }
            )

            return

        try:

            content_length = int(
                self.headers.get(
                    "Content-Length",
                    0
                )
            )

            body = self.rfile.read(
                content_length
            )

            data = json.loads(
                body.decode("utf-8")
            )

            user_message = data.get(
                "message",
                ""
            ).strip()

            if not user_message:

                self.send_json(
                    400,
                    {
                        "error":
                            "Message cannot be empty."
                    }
                )

                return

            print(
                f"[EVA] Command received: "
                f"{user_message}"
            )

            # ==========================================
            # RESET SPEECH BRIDGE
            # ==========================================

            reset_speech_event()

            # ==========================================
            # RUN EXISTING ROUTER IN BACKGROUND
            # ==========================================

            router_result = {
                "handled": False
            }

            def run_router():

                try:

                    router_result["handled"] = (
                        router.process(
                            user_message
                        )
                    )

                except Exception as e:

                    print(
                        "[EVA] Router error:",
                        e
                    )

            router_thread = threading.Thread(
                target=run_router,
                daemon=True
            )

            router_thread.start()

            # ==========================================
            # WAIT FOR COMMAND RESPONSE
            # ==========================================

            speech_started = (
                speech_started_event.wait(
                    timeout=2
                )
            )

            # ==========================================
            # COMMAND HANDLER SPOKE
            # ==========================================

            if speech_started:

                reply = get_last_spoken_text()

                print(
                    "[EVA] Router response:",
                    reply
                )

                self.send_json(
                    200,
                    {
                        "reply": reply,
                        "handled": True
                    }
                )

                return

            # ==========================================
            # ROUTER FINISHED WITHOUT SPEAKING
            # ==========================================

            router_thread.join(
                timeout=0.1
            )

            if router_result["handled"]:

                reply = (
                    get_last_spoken_text()
                    or "Command completed."
                )

                self.send_json(
                    200,
                    {
                        "reply": reply,
                        "handled": True
                    }
                )

                return

            # ==========================================
            # AI BRAIN FALLBACK
            # ==========================================

            print(
                "[EVA] No command handler matched."
            )

            reply = ai_brain.ask_eva(
                user_message
            )

            # ==========================================
            # SEND TEXT TO FLUTTER FIRST
            # ==========================================

            self.send_json(
                200,
                {
                    "reply": reply,
                    "handled": False
                }
            )

            # ==========================================
            # SPEAK AI RESPONSE
            # ==========================================

            threading.Thread(
                target=speak,
                args=(reply,),
                daemon=True
            ).start()

        except json.JSONDecodeError:

            self.send_json(
                400,
                {
                    "error": "Invalid JSON."
                }
            )

        except Exception as e:

            print(
                "API Error:",
                e
            )

            self.send_json(
                500,
                {
                    "error":
                        "EVA encountered "
                        "an internal error."
                }
            )

    def log_message(self, format, *args):

        print(
            f"[API] "
            f"{self.address_string()} - "
            f"{format % args}"
        )


def start_server():

    server = HTTPServer(
        (HOST, PORT),
        EvaAPIHandler
    )

    print("=" * 55)
    print("EVA API SERVER")
    print("=" * 55)

    print(
        f"Server running at "
        f"http://{HOST}:{PORT}"
    )

    print(
        "Chat endpoint: POST /chat"
    )

    print(
        "Listen endpoint: POST /listen"
    )

    print(
        "Startup endpoint: GET /startup"
    )

    print(
        "Existing command router: ENABLED"
    )

    print(
        "AI brain fallback: ENABLED"
    )

    print(
        "EVA is ready for Flutter."
    )

    print("=" * 55)

    try:

        server.serve_forever()

    except KeyboardInterrupt:

        print(
            "\nStopping EVA API server..."
        )

    finally:

        server.server_close()


if __name__ == "__main__":
    start_server()