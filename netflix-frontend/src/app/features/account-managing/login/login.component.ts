import {Component, signal} from '@angular/core';
import {FormBuilder, FormGroup, ReactiveFormsModule, Validators} from "@angular/forms";
import {CognitoService} from "../../../core/services/cognito/cognito.service";
import {NgIf} from "@angular/common";
import {Router, RouterLink} from "@angular/router";

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    NgIf,
    ReactiveFormsModule,
    RouterLink
  ],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss'
})
export class LoginComponent {
  form!: FormGroup;
  submitted = false;
  get f() { return this.form.controls; }
  constructor (private cognitoService:CognitoService,
               private formBuilder: FormBuilder,
               private router: Router) { }

  ngOnInit() {
    this.form = this.formBuilder.group({
      username: ['', Validators.required],
      password: ['',Validators.required]
    });
  }

  async onSubmit() {
    this.submitted=true
    var username: string = this.f['username'].value
    var password: string = this.f['password'].value

    var signedIn = await this.cognitoService.signIn(username, password)
    if (!signedIn) {
      this.form.controls['password'].setErrors({'incorrect': true});
      return;
    }

    this.router.navigate([''])

  }
}
