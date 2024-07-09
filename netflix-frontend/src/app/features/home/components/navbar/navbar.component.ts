import { Component } from '@angular/core';
import {AuthService} from "../../../../core/services/auth/auth.service";
import {NgIf} from "@angular/common";
import {CognitoService} from "../../../../core/services/cognito/cognito.service";
import {NavigationEnd, Router, RouterLink} from "@angular/router";

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [
    NgIf,
    RouterLink
  ],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})
export class NavbarComponent {
  role:string[]|undefined|null
  constructor(private cognitoService:CognitoService, private router:Router) {

  }

  async ngOnInit() {
    this.role = await this.cognitoService.getUserGroup()
    console.log(this.role)
    console.log('aa')
    var url=this.router.url
    url=url.split('?')[0].split('/').pop()!
    url=String(url)

    if(!(url==='login' || url==='registration') && this.role==null){
      this.router.navigate(['login'])
    }
  }

  async signOut() {
    await this.cognitoService.signOut()
    console.log('sss')
    // location.reload();
    this.router.navigate(['login'])
  }

}
