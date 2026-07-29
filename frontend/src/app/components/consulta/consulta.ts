import { Component, ChangeDetectorRef } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

import { Polizas } from '../../services/polizas';
import { AuthService } from '../../services/auth';

@Component({
  selector: 'app-consulta',
  imports: [FormsModule],
  templateUrl: './consulta.html',
  styleUrl: './consulta.css',
})
export class Consulta {
  numero = '';
  poliza: any = null;
  coberturas: any[] = [];
  mensaje = '';
  esError = false;

  constructor(
    private polizasService: Polizas,
    private auth: AuthService,
    private router: Router,
    private cdr: ChangeDetectorRef
  ) {}

  buscarPoliza() {
    this.polizasService.consultarPoliza(this.numero).subscribe({
      next: (data) => {
        this.poliza = data;
        this.mensaje = '';
        this.esError = false;
        this.buscarCoberturas();
      },
      error: () => {
        this.poliza = null;
        this.coberturas = [];
        this.mensaje = 'No se encontró la póliza.';
        this.esError = true;
        this.cdr.detectChanges();
      },
    });
  }

  buscarCoberturas() {
    this.polizasService.listarCoberturas(this.numero).subscribe({
      next: (data) => {
        this.coberturas = data;
        this.cdr.detectChanges();
      },
      error: () => {
        this.coberturas = [];
        this.cdr.detectChanges();
      },
    });
  }

  crearConsumo(coberturaId: number) {
    this.polizasService.registrarConsumo(this.numero, coberturaId).subscribe({
      next: (data) => {
        this.mensaje = data.detail;
        this.esError = false;
        this.buscarCoberturas();
      },
      error: (error) => {
        this.mensaje = error.error.detail;
        this.esError = true;
        this.cdr.detectChanges();
      },
    });
  }

  cerrarSesion() {
    this.auth.logout();
    this.router.navigate(['/login']);
  }
}
