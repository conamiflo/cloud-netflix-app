import { Component } from '@angular/core';
import {CognitoService} from "../../../core/services/cognito/cognito.service";
import {FormBuilder, FormGroup, ReactiveFormsModule, Validators} from "@angular/forms";
import {CommonModule, NgClass, NgIf} from "@angular/common";
import {UserDTO} from "../../../core/models/UserDTO";

@Component({
  selector: 'app-registration',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    NgClass,
    NgIf
  ],
  templateUrl: './registration.component.html',
  styleUrl: './registration.component.scss'
})
export class RegistrationComponent {
  form!: FormGroup;
  submitted = false;
  get f() { return this.form.controls; }
  constructor (private cognitoService:CognitoService,
               private formBuilder: FormBuilder,
  ) {

  }

  ngOnInit() {
    this.form = this.formBuilder.group({
      name: ['', Validators.required],
      family_name: ['', Validators.required],
      phone_number: ['', [Validators.required, Validators.pattern( "^\\+[1-9][0-9]{0,24}$" )]],
      email: ['', [Validators.required, Validators.email]],
      username: ['', Validators.required],
      password: ['',[Validators.required,Validators.pattern(/^(?!\s+)(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[\^$*.[\]{}()?"!@#%&/\\,><':;|_~`=+-]).{8,256}(?<!\s)$/
      )]]
    });
  }
  onSubmit(){
    this.submitted=true;

    if (!this.form.valid) {
      return
    }

    var name:string=this.form.controls['name'].value
    var family_name:string=this.form.controls['family_name'].value
    var username:string=this.form.controls['username'].value
    var phone_number:number=this.form.controls['phone_number'].value
    var email:string=this.form.controls['email'].value
    var password:string=this.form.controls['password'].value

    var user:UserDTO=new UserDTO(username,name,email,password,phone_number,family_name)

    this.cognitoService.signUp(user)



  }
}
