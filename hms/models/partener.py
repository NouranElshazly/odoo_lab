from odoo import models, fields, api   
from odoo.exceptions import UserError, ValidationError

class HmsPartener(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one('hms.patient', string='Related Patient')
    vat = fields.Char(required=True)

    @api.constrains('email')
    def _check_email_not_in_patients(self):
        for rec in self:
            if rec.email:
                patient = self.env['hms.patient'].search([('email', '=', rec.email)], limit=1)
                if patient:
                    raise ValidationError("This email already exists in a patient record. Cannot assign same email.")

    def unlink(self):
        for rec in self:
            if rec.related_patient_id:
                raise ValidationError("Cannot delete a customer linked to a patient.")
        return super().unlink()