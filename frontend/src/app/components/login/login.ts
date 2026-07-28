import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth';

@Component({
  selector: 'app-login',
  imports: [FormsModule],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login {
  username = '';
  password = '';
  mensaje = '';

  constructor(private authService: AuthService) {}

  onLogin() {
    this.authService.login(this.username, this.password).subscribe({
      next: (response) => {
        this.mensaje = 'Inicio de sesión exitoso';
      },
      error: (error) => {
        this.mensaje = 'Error al iniciar sesión';
      }
    });
  }
}
