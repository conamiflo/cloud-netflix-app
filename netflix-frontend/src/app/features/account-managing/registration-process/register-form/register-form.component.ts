import {FormBuilder, FormGroup, ReactiveFormsModule, Validators} from "@angular/forms";
import {CognitoService} from "../../../../core/services/cognito/cognito.service";
import {Component, EventEmitter, Output} from '@angular/core';
import {CommonModule, NgClass, NgIf} from "@angular/common";
import {UserDTO} from "../../../../core/models/UserDTO";
import {Router, RouterLink} from "@angular/router";

@Component({
  selector: 'app-register-form',
  standalone: true,
  imports: [
    NgIf,
    CommonModule,
    NgClass,
    ReactiveFormsModule,
    RouterLink
  ],
  templateUrl: './register-form.component.html',
  styleUrl: './register-form.component.scss'
})
export class RegisterFormComponent {
  @Output() onSuccReg = new EventEmitter<any>();

  form!: FormGroup;
  submitted = false;
  user_taken: boolean=false;
  email_taken: boolean=false;

  get f() { return this.form.controls; }
  constructor (private cognitoService:CognitoService,
               private formBuilder: FormBuilder,
               private router: Router
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
  async onSubmit() {
    this.submitted = true;
    this.user_taken=false;
    this.email_taken=false;

    if (!this.form.valid) {
      return
    }

    var name: string = this.form.controls['name'].value
    var family_name: string = this.form.controls['family_name'].value
    var username: string = this.form.controls['username'].value
    var phone_number: number = this.form.controls['phone_number'].value
    var email: string = this.form.controls['email'].value
    var password: string = this.form.controls['password'].value

    var user: UserDTO = new UserDTO(username, name, email, password, phone_number, family_name)

    var err:string = await this.cognitoService.signUp(user)

    err=String(err)

    console.log(err)

    if(err.includes("UserLambdaValidationException")){
      this.form.controls['email'].setErrors({'incorrect': true});
      this.email_taken=true;
    }
    else if(err.includes("UsernameExistsException")){
      this.form.controls['username'].setErrors({'incorrect': true});
      this.user_taken=true;
    }
    else if(err.includes("phone")){
      this.form.controls['phone_number'].setErrors({'incorrect': true});
    }else if(err===''){
      this.onSuccReg.emit(username);
    }



    // if (!succ) {
    //   this.form.controls['username'].setErrors({'incorrect': true});
    //   return;
    // }
    //
    // this.onSuccReg.emit(username);

    //this.router.navigate([''])


  }
}
