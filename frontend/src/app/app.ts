import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import {Login} from './components/login/login';
import {Consulta} from './components/consulta/consulta';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, Login, Consulta],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('frontend');
}
