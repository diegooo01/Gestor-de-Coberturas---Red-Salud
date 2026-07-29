import { TestBed } from '@angular/core/testing';

import { Polizas } from './polizas';

describe('Polizas', () => {
  let service: Polizas;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Polizas);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
