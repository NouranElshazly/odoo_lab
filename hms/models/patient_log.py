
from odoo import models, fields

class HmsPatientLog(models.Model):
    _name = 'hms.patient.log'
    _description = 'Patient Log History'

    created_by = fields.Many2one('res.users', default=lambda self: self.env.user)
    date = fields.Datetime(default=fields.Datetime.now)
    description = fields.Text()
    patient_id = fields.Many2one('hms.patient')
