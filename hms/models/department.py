from odoo import  models,fields ,api

class HmsDepartment(models.Model):
    _name = 'hms.department'
    _description = 'Hospital Department'

    name = fields.Char(required=True)
    capacity = fields.Integer()
    is_opened = fields.Boolean(default=True)
    patient_id = fields.One2many('hms.patient', 'department_id', string='Patients')
