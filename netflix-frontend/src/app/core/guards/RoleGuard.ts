import {
  ActivatedRouteSnapshot,
  CanActivate,
  RouterStateSnapshot,
  UrlTree
} from '@angular/router';
import { Observable } from 'rxjs';
import { AuthService } from '../services/auth/auth.service';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class RoleGuard implements CanActivate {
  constructor(private authService: AuthService) {}

  async canActivate(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): Promise<boolean | UrlTree> {
    const allowedRoles = next.data['roles'] as Array<string>;

    // Assuming `hasAnyRole` is an async method in `AuthService`
    const hasRole = await this.authService.hasAnyRole(allowedRoles);

    // If the user has any of the allowed roles, return true, otherwise redirect to unauthorized page
    if (hasRole) {
      return true;
    } else {
      // Here you should handle the redirection to an unauthorized page or return an UrlTree
      return false;
    }
  }
}
