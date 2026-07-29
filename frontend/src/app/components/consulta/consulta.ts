import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { Polizas } from '../../services/polizas';

@Component({
  selector: 'app-consulta',
  imports: [FormsModule],
  templateUrl: './consulta.html',
  styleUrl: './consulta.css',
})
export class Consulta {
  numero = '';
  poliza: any = null;
  mensaje = '';

  constructor(private polizasService: Polizas) {}

  buscarPoliza(){
    this.polizasService.consultarPoliza(this.numero).subscribe({
      next: (data) => {
        this.poliza = data;
        this.mensaje = '';
      },
      error: (error) => {
        this.poliza = null;
        this.mensaje = 'No se encontró la poliza.';
      }
    });
  }

  buscarCoberturas(){
    this.polizasService.listarCoberturas(this.numero).subscribe({
      next: (data) => {
        if (this.poliza) {
          this.poliza.coberturas = data;
        }
        this.mensaje = '';
      },
      error: (error) => {
        this.mensaje = 'No se encontraron coberturas.';
      }
    });
  }

  crearConsumo(coberturaId: number){
    this.polizasService.registrarConsumo(this.numero, coberturaId).subscribe({
      next: (data) => {
        this.mensaje = data.detail;
        this.buscarCoberturas();
      },
      error: (error) => {
        this.mensaje = error.error.detail;
      }
    });
  }
}
