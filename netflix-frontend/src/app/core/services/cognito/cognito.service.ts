import { Injectable } from '@angular/core';
import {environment} from "../../../../environments/environment";
import {UserDTO} from "../../models/UserDTO";
import {Router} from "@angular/router";
import { Amplify, Auth } from 'aws-amplify';
// @ts-ignore
import awsconfig from '../../../../../src/aws-exports.js';
import {angularJitApplicationTransform} from "@angular/compiler-cli";
Amplify.configure(awsconfig);

//@angularJitApplicationTransform(mod16)

@Injectable({
  providedIn: 'root'
})
export class CognitoService {

  constructor(private router: Router) {}
  async signUp(usr:UserDTO) {
    var username=usr.username
    var password=usr.password
    var phone_number=usr.phone_number
    var email=usr.email
    var name=usr.name
    var family_name=usr.family_name
    try {
      const { user } = await Auth.signUp({
        username,
        password,
        attributes: {
          email, // optional
          phone_number, // optional - E.164 number convention
          name,// other custom attributes
          family_name
        },
        autoSignIn: {
          // optional - enables auto sign in after user is confirmed
          enabled: false
        }
      });
      console.log(user);
    } catch (error) {
      console.log('error signing up:', error);
    }
  }
}
