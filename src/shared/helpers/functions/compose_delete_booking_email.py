from datetime import datetime
from src.shared.domain.entities.booking import Booking


def compose_deleted_user_email(user, deleted_booking: Booking):
    name = user.get('name')
    email = user.get('email')
    data_hora_inicio = datetime.fromtimestamp(deleted_booking.start_date/1000)
    data_hora_fim = datetime.fromtimestamp(deleted_booking.end_date/1000)

    message = f"""
        <!doctype html>
        <html lang="pt-BR">
          <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>Reserva Cancelada</title>
            <style>
              * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
              }}

              body {{
                font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f5f5f5;
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
              }}

              .card {{
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
                max-width: 600px;
                width: 100%;
                overflow: hidden;
                position: relative;
              }}

              .header {{
                background: linear-gradient(135deg, #ff6b6b, #ff8e8e);
                color: white;
                padding: 30px 20px;
                text-align: center;
                position: relative;
              }}

              .header h1 {{
                font-size: 28px;
                font-weight: bold;
                margin: 0;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
              }}

              .court-image {{
                width: 100%;
                height: 200px;
                object-fit: cover;
                background: linear-gradient(45deg, #4a9eff, #2ecc71);
                position: relative;
              }}

              .court-placeholder {{
                width: 100%;
                height: 200px;
                background: linear-gradient(135deg, #4a9eff, #2ecc71);
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 18px;
                font-weight: bold;
              }}

              .content {{
                padding: 40px 30px;
                text-align: center;
              }}

              .greeting {{
                font-size: 24px;
                color: #2c3e50;
                margin-bottom: 20px;
                font-weight: 600;
              }}

              .message {{
                font-size: 18px;
                color: #555;
                margin-bottom: 25px;
                line-height: 1.4;
              }}

              .reservation-details {{
                background: #f8f9fa;
                border-radius: 15px;
                padding: 25px;
                margin: 25px 0;
                border-left: 5px solid #ff6b6b;
              }}

              .detail-item {{
                margin: 10px 0;
                font-size: 16px;
              }}

              .detail-label {{
                font-weight: bold;
                color: #2c3e50;
              }}

              .detail-value {{
                color: #555;
              }}

              .cancelled-notice {{
                font-size: 20px;
                font-weight: bold;
                color: #e74c3c;
                margin: 20px 0;
                padding: 15px;
                background: #ffeaea;
                border-radius: 10px;
                border: 2px solid #ff6b6b;
              }}

              .reason {{
                font-size: 16px;
                color: #555;
                margin: 20px 0;
                font-weight: 600;
              }}

              .contact-info {{
                font-size: 16px;
                color: #666;
                margin: 25px 0;
                line-height: 1.5;
              }}

              .contact-link {{
                color: #3498db;
                text-decoration: underline;
                font-weight: 600;
              }}

              .footer {{
                border-top: 1px solid #eee;
                padding: 30px;
                text-align: center;
                background: #fafafa;
              }}

              .logo {{
                width: 60px;
                height: 60px;
                background: linear-gradient(135deg, #3498db, #2ecc71);
                border-radius: 15px;
                margin: 0 auto 15px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 24px;
                font-weight: bold;
              }}

              .signature {{
                font-size: 16px;
                color: #555;
                margin: 5px 0;
              }}

              .team-name {{
                font-weight: bold;
                color: #2c3e50;
              }}

              .site-name {{
                color: #666;
                font-size: 14px;
                margin-top: 10px;
              }}

              @media (max-width: 600px) {{
                .card {{
                  margin: 10px;
                  border-radius: 15px;
                }}

                .content {{
                  padding: 30px 20px;
                }}

                .header h1 {{
                  font-size: 24px;
                }}

                .greeting {{
                  font-size: 20px;
                }}
              }}
            </style>
          </head>
          <body>
            <div class="card">
              <div class="header">
                <h1>Reserva Cancelada!</h1>
              </div>

              <img src="court-image.jpg" alt="Quadra" />

              <div class="content">
                <div class="greeting">Olá {name},</div>

                <div class="message">Lamentamos informar que sua reserva:</div>

                <div class="reservation-details">
                  <div class="detail-item">
                    <span class="detail-label">Quadra:</span>
                    <span class="detail-value">{deleted_booking.court_number}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Data:</span>
                    <span class="detail-value">{data_hora_inicio.strftime("%d/%m/%Y")}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Horário:</span>
                    <span class="detail-value">{data_hora_inicio.strftime("%H:%M")} - {data_hora_fim.strftime("%H:%M")}</span>
                  </div>
                </div>

                <div class="cancelled-notice">foi cancelada!!</div>

              </div>

              <div class="footer">
                <img src="logo.png" alt="Logo" />
                <div class="signature">Atenciosamente,</div>
                <div class="signature team-name">Equipe Reservation</div>
                <div class="site-name">
                  <a href="https://reservation.devmaua.com" target="_blank"
                    >reservation.devmaua.com</a
                  >
                </div>
              </div>
            </div>
          </body>
        </html>
        """

    message = message.format(name=name)

    return message