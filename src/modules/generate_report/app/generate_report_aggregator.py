from src.shared.domain.entities.booking import Booking
from .generate_report_extractor import GenerateReportExtractor
from typing import List


class GenerateReportAggregator:

    def __init__(self, extractor: GenerateReportExtractor):
        self.extractor = extractor

    def __call__(self, initial_date, final_date):

        bookings = self.extractor(initial_date, final_date)

        #fazer logica aqui
        #trocar os bookings por users
        #dps instalar as dependencias do requirements-dev.txt
        

        users_statistics = {}

        for booking in bookings:
            if booking.user_id not in users_statistics:
                users_statistics[booking.user_id] = {
                    "reservas_feitas": 0,
                    "Tennis": 0,
                    "Football": 0,
                    "Basketball": 0,
                    "Volleyball": 0,
                    "Handball": 0,
                    "Futsal": 0,
                    "Rugby": 0,
                    "Ping Pong": 0,
                    1: 0,
                    2: 0,
                    3: 0,
                    4: 0,
                    5: 0,
                    "tempo_em_quadra": 0
                }

            users_statistics[booking.user_id]["reservas_feitas"] += 1
            users_statistics[booking.user_id][booking.sport.value] += 1
            users_statistics[booking.user_id][booking.court_number] += 1
            users_statistics[booking.user_id]["tempo_em_quadra"] += booking.end_date - booking.start_date


        #court statistics logic
        court_statistics = {}

        for booking in bookings:
            court_key = booking.court_number

            if court_key not in court_statistics:
                court_statistics[court_key] = {
                    "reservas_feitas": 0,
                    "tempo_de_uso": 0,
                    "Tennis": 0,
                    "Football": 0,
                    "Basketball": 0,
                    "Volleyball": 0,
                    "Handball": 0,
                    "Futsal": 0,
                    "Rugby": 0,
                    "Ping Pong": 0
                }

            sport_column = booking.sport.value
            if sport_column not in court_statistics[court_key]:
                court_statistics[court_key][sport_column] = 0

            user_column = f"user_{booking.user_id}"
            if user_column not in court_statistics[court_key]:
                court_statistics[court_key][user_column] = 0

            court_statistics[court_key]["reservas_feitas"] += 1
            court_statistics[court_key]["tempo_de_uso"] += (booking.end_date - booking.start_date)
            court_statistics[court_key][sport_column] += 1
            court_statistics[court_key][user_column] += 1


        #sport_statistics logic
        sport_statistics = {}

        for booking in bookings:
            sport_key = booking.sport.value

            # Se ainda não existir, inicializa
            if sport_key not in sport_statistics:
                sport_statistics[sport_key] = {
                    "Reservas Feitas": 0,
                    "quadra 1": 0,
                    "quadra 2": 0,
                    "quadra 3": 0,
                    "quadra 4": 0,
                    "quadra 5": 0,
                    "Tempo Total Praticado": 0,
                }

                # Atualiza os valores
                sport_statistics[sport_key]["Reservas Feitas"] += 1
                sport_statistics[sport_key][f"quadra {booking.court_number}"] += 1
                sport_statistics[sport_key]["Tempo Total Praticado"] += (booking.end_date - booking.start_date)

                user_column = f"Usuário: {booking.user_id}"
                if user_column not in sport_statistics[sport_key]:
                    sport_statistics[sport_key][user_column] = 0

                sport_statistics[sport_key][user_column] += 1

                #sport_statistics logic

        return users_statistics, court_statistics, sport_statistics
