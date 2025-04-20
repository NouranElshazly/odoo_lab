from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import date

class HmsPatient(models.Model):
    _name = 'hms.patient'
    _description = 'Hospital Patient'

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    email = fields.Char()
    birth_date = fields.Date()
    history = fields.Html()
    cr_ratio = fields.Float('CR Ratio')
    blood_type = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('ab', 'AB'),
        ('o', 'O'),
    ], string='Blood Type')
    pcr = fields.Boolean('PCR')
    image = fields.Binary('Image')
    address = fields.Text()
    age = fields.Integer(compute="_compute_age", store=True)
    state = fields.Selection([('undetermined', 'Undetermined'),('good', 'Good'),('fair', 'Fair'),('serious','Serious')], default='undetermined')

    department_id = fields.Many2one('hms.department' , string='Department',default=lambda self: self.env['hms.department'].search([('is_opened', '=', True)], limit=1))
    doctor_ids = fields.Many2many('hms.doctor', string='Doctors')
    log_ids = fields.One2many('hms.patient.log', 'patient_id', string='Logs')
    doctor_id = fields.Many2one('hms.doctor' , string='Doctor')


    @api.constrains("email")
    def _check_email(self):
        for rec in self:
            if rec.email and not rec.email.endswith('@gmail.com'):
                raise ValidationError("Email must end with @gmail.com")
            exists_email = self.env['hms.patient'].search([('email', '=', rec.email), ('id', '!=', rec.id)])
            if exists_email:
                raise ValidationError("Email must be unique")

    @api.depends('birth_date')
    def _compute_age(self):
        for rec in self:
            if rec.birth_date:
                today = date.today()
                rec.age = today.year - rec.birth_date.year
                if today.month < rec.birth_date.month or (today.month == rec.birth_date.month and today.day < rec.birth_date.day):
                    rec.age -= 1
            else:
                rec.age = 0

    @api.onchange('age')
    def _onchange_age(self):
        if self.age < 30:
            self.pcr = True
            return {'warning': {'title': 'PCR Checked', 'message': 'PCR has been automatically checked due to age < 30'}}
        if self.age < 50:
            return {'domain': {'history': [('invisible', True)]}}

    @api.onchange('department_id')
    def _onchange_department(self):
        if not self.department_id.is_opened:
            raise UserError("You can't select a closed department.")

    
    @api.model
    def create(self, vals):
        res = super().create(vals)
        if vals.get('state'):
            self.env['hms.patient.log'].create({
                'patient_id': res.id,
                'description': f"State changed to {vals['state']}",
                'created_by': self.env.user.id,
            })
        return res

    def write(self, vals):
        if 'state' in vals:
            for record in self:
                self.env['hms.patient.log'].create({
                    'patient_id': record.id,
                    'description': f"State changed to {vals['state']}",
                    'created_by': self.env.user.id,
                })
        return super().write(vals)




    @api.constrains('pcr', 'cr_ratio')
    def _check_cr_ratio_required(self):
        for rec in self:
            if rec.pcr and not rec.cr_ratio:
                raise ValidationError("CR Ratio is required when PCR is checked.")