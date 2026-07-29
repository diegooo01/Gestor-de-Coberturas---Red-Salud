import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class Polizas {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  consultarPoliza(numero: string): Observable<any>{
    return this.http.get<any>(`${this.apiUrl}/polizas/${numero}/`);
  }

  listarCoberturas(numero: string): Observable<any>{
    return this.http.get<any>(`${this.apiUrl}/polizas/${numero}/coberturas/`);
  }

  registrarConsumo(numero: string, coberturaId: number): Observable<any>{
    return this.http.post<any>(`${this.apiUrl}/polizas/${numero}/consumos/`, { coberturaId: coberturaId });
  }
}
