from odoo import models,fields,api

class HmsDoctor(models.Model):
    _name = 'hms.doctor'
    _description = 'Hospital Doctor'

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    image = fields.Binary('Image')
    patient_ids = fields.One2many('hms.patient', 'doctor_id', string='Patients')

