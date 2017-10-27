# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Asignacion(models.Model):
    clase = models.CharField(max_length=20)
    puesto = models.CharField(max_length=10)
    alumno = models.CharField(max_length=60)
    ordenador = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'asignacion'
        unique_together = (('clase', 'puesto'),)


class Cd(models.Model):
    idcd = models.AutoField(primary_key=True)
    vendor = models.CharField(max_length=45, blank=True, null=True)
    product = models.CharField(max_length=70, blank=True, null=True)
    equipo_num_serie = models.ForeignKey('Equipo', models.DO_NOTHING, db_column='equipo_num_serie')

    class Meta:
        managed = False
        db_table = 'cd'


class CloudDns(models.Model):
    ip = models.IntegerField()
    host = models.CharField(max_length=30)
    dominio = models.CharField(max_length=40)
    usuario = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'cloud_dns'


class Cpu(models.Model):
    idcpu = models.AutoField(primary_key=True)
    vendor = models.CharField(max_length=45, blank=True, null=True)
    product = models.CharField(max_length=70, blank=True, null=True)
    slot = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cpu'


class Equipo(models.Model):
    num_serie = models.CharField(primary_key=True, max_length=45)
    vendor = models.CharField(max_length=45, blank=True, null=True)
    product = models.CharField(max_length=70, blank=True, null=True)
    cpu_idcpu = models.ForeignKey(Cpu, models.DO_NOTHING, db_column='cpu_idcpu')

    class Meta:
        managed = False
        db_table = 'equipo'


class Hd(models.Model):
    serial = models.CharField(max_length=45)
    equipo_num_serie = models.ForeignKey(Equipo, models.DO_NOTHING, db_column='equipo_num_serie')
    vendor = models.CharField(max_length=45, blank=True, null=True)
    product = models.CharField(max_length=70, blank=True, null=True)
    description = models.CharField(max_length=45, blank=True, null=True)
    size = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hd'
        unique_together = (('serial', 'equipo_num_serie'),)


class Incidencias(models.Model):
    fecha = models.CharField(max_length=10)
    ordenador = models.CharField(max_length=15)
    incidencia = models.TextField()
    estado = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'incidencias'


class Matricula(models.Model):
    alumno = models.CharField(max_length=30)
    codasig = models.IntegerField()
    tipo = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'matricula'


class Modulos(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    codigo = models.CharField(db_column='Codigo', max_length=15)  # Field name made lowercase.
    curso = models.CharField(db_column='Curso', max_length=16)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=70)  # Field name made lowercase.
    horas = models.IntegerField(db_column='Horas')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'modulos'


class Ram(models.Model):
    idram = models.AutoField(primary_key=True)
    size = models.CharField(max_length=45, blank=True, null=True)
    clock = models.CharField(max_length=45, blank=True, null=True)
    equipo_num_serie = models.ForeignKey(Equipo, models.DO_NOTHING, db_column='equipo_num_serie')

    class Meta:
        managed = False
        db_table = 'ram'


class Red(models.Model):
    serial = models.CharField(max_length=45)
    equipo_num_serie = models.ForeignKey(Equipo, models.DO_NOTHING, db_column='equipo_num_serie')
    vendor = models.CharField(max_length=45, blank=True, null=True)
    product = models.CharField(max_length=70, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'red'
        unique_together = (('serial', 'equipo_num_serie'),)
