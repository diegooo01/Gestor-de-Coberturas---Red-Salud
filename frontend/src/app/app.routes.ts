import { Routes } from '@angular/router';

import { Login } from './components/login/login';
import { Consulta } from './components/consulta/consulta';
import {authGuard} from './guards/auth-guard';

export const routes: Routes = [
  { path: 'login', component: Login },
  { path: 'consulta', component: Consulta, canActivate: [authGuard] },
  { path: '', redirectTo: 'login', pathMatch: 'full' },
];
