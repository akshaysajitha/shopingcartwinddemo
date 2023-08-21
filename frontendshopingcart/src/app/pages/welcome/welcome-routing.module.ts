import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { WelcomeComponent } from './welcome.component';
import { CartComponent } from './container/cart/cart.component';
import { OrderplacedComponent } from './completeorder/orderplaced/orderplaced.component';
const routes: Routes = [
  { path: '', component: WelcomeComponent },
  {path:'cart',component:CartComponent},
  {path:'orderplaced',component:OrderplacedComponent}

];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class WelcomeRoutingModule { }
