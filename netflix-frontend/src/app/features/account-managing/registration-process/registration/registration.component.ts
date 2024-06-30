import { Component } from '@angular/core';
import {CognitoService} from "../../../../core/services/cognito/cognito.service";
import {FormBuilder, FormGroup, ReactiveFormsModule, Validators} from "@angular/forms";
import {CommonModule, NgClass, NgIf} from "@angular/common";
import {UserDTO} from "../../../../core/models/UserDTO";
import {Router} from "@angular/router";
import {RegisterFormComponent} from "../register-form/register-form.component";
import {EmailConfirmComponent} from "../email-confirm/email-confirm.component";

@Component({
  selector: 'app-registration',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    NgClass,
    NgIf,
    RegisterFormComponent,
    EmailConfirmComponent
  ],
  templateUrl: './registration.component.html',
  styleUrl: './registration.component.scss'
})
export class RegistrationComponent {

  username:any=null;

}
