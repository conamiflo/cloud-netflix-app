import {booleanAttribute, Component, Input} from '@angular/core';
import {FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators} from "@angular/forms";
import {NgClass, NgIf} from "@angular/common";
import {CognitoService} from "../../../../core/services/cognito/cognito.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-email-confirm',
  standalone: true,
  imports: [
    FormsModule,
    NgIf,NgClass,
    ReactiveFormsModule
  ],
  templateUrl: './email-confirm.component.html',
  styleUrl: './email-confirm.component.scss'
})
export class EmailConfirmComponent {
  @Input() username:any;
  form!: FormGroup;
  submitted = false;
  success=false
  get f() { return this.form.controls; }
  constructor (private cognitoService:CognitoService,
               private formBuilder: FormBuilder,
               private router: Router
  ) {

  }

  ngOnInit() {
    this.form = this.formBuilder.group({
      code: ['', Validators.required],
    });
  }

  async onSubmit() {
    this.submitted = true;
    if (!this.form.valid) {
      return
    }

    var code = this.f['code'].value
    var valid: boolean = await this.cognitoService.confirmSignUp(this.username, code)

    if (!valid) {
      this.form.controls['code'].setErrors({'incorrect': true});
      return;
    }
    this.form.controls['code'].setErrors(null);
    this.success=true

  }
}
