from flask import Blueprint, request, jsonify
from backend.models.Report import Report
from backend.extensions import db

routes_bp = Blueprint('reports', __name__)


# Получение списка всех отчетов
@routes_bp.route('/reports', methods=['GET'])
def get_reports():
    reports = Report.query.all()
    return jsonify([report.serialize() for report in reports])


# Получение отчета по ID
@routes_bp.route('/reports/<int:id>', methods=['GET'])
def get_report(id):
    report = Report.query.get(id)
    if report is None:
        return jsonify({'message': 'Report not found'}), 404
    return jsonify(report.serialize())


# Создание нового отчета
@routes_bp.route('/reports', methods=['POST'])
def create_report():
    data = request.get_json()

    # Проверка на наличие всех обязательных данных в запросе
    required_fields = ['name', 'report_date', 'user_role',
                       'oil_production', 'gas_production', 'avg_well_debit',
                       'equipment_failures', 'downtime_hours', 'electricity_cost', 'total_cost']

    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing required field: {field}'}), 400

    new_report = Report(
        name=data['name'],
        report_date=data['report_date'],
        user_role=data['user_role'],
        oil_production=data['oil_production'],
        gas_production=data['gas_production'],
        avg_well_debit=data['avg_well_debit'],
        equipment_failures=data['equipment_failures'],
        downtime_hours=data['downtime_hours'],
        electricity_cost=data['electricity_cost'],
        total_cost=data['total_cost']
    )

    try:
        # Сохранение нового отчета в базу данных
        db.session.add(new_report)
        db.session.commit()
        return jsonify(new_report.serialize()), 201  # Вернем сериализованные данные и статус 201
    except Exception as e:
        db.session.rollback()  # В случае ошибки откатим изменения
        return jsonify({'message': str(e)}), 500


# Обновление отчета
@routes_bp.route('/reports/<int:id>', methods=['PUT'])
def update_report(id):
    data = request.get_json()
    report = Report.query.get(id)
    if report is None:
        return jsonify({'message': 'Report not found'}), 404

    # Обновление полей отчета с учетом новых данных
    report.name = data.get('name', report.name)
    report.report_date = data.get('report_date', report.report_date)
    report.user_role = data.get('user_role', report.user_role)
    report.oil_production = data.get('oil_production', report.oil_production)
    report.gas_production = data.get('gas_production', report.gas_production)
    report.avg_well_debit = data.get('avg_well_debit', report.avg_well_debit)
    report.equipment_failures = data.get('equipment_failures', report.equipment_failures)
    report.downtime_hours = data.get('downtime_hours', report.downtime_hours)
    report.electricity_cost = data.get('electricity_cost', report.electricity_cost)
    report.total_cost = data.get('total_cost', report.total_cost)

    db.session.commit()
    return jsonify(report.serialize())


# Удаление отчета
@routes_bp.route('/reports/<int:id>', methods=['DELETE'])
def delete_report(id):
    report = Report.query.get(id)
    if report is None:
        return jsonify({'message': 'Report not found'}), 404

    db.session.delete(report)
    db.session.commit()
    return jsonify({'message': 'Report deleted'}), 200
