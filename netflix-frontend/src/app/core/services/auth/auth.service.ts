import { Injectable } from '@angular/core';
import {CognitoService} from "../cognito/cognito.service";

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private cognitoService:CognitoService) { }

  async hasAnyRole(allowedRoles: string[]): Promise<boolean> {

    var user = await this.cognitoService.getUser()

    if(Object.keys(user).length===0){
      return false;
    }

    if(allowedRoles.length==0){
      return true;//8io

    }

    var roles:string[] = await this.cognitoService.getUserGroup();

    for (const role of roles) {
      if (allowedRoles.includes(role)) {
        return true;
      }
    }
    return false;
  }

}
