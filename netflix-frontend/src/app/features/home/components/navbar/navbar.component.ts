import { Component } from '@angular/core';
import {AuthService} from "../../../../core/services/auth/auth.service";
import {NgIf} from "@angular/common";
import {CognitoService} from "../../../../core/services/cognito/cognito.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [
    NgIf
  ],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})
export class NavbarComponent {
  role:string[]|null
  constructor(private cognitoService:CognitoService) {

  }

  async ngOnInit() {
    this.role = await this.cognitoService.getUserGroup()
    console.log(this.role)
  }

  async signOut() {
    await this.cognitoService.signOut()
    console.log('sss')
    location.reload();

  }



}
