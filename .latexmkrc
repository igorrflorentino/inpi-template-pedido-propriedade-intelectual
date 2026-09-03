add_cus_dep( 'glo', 'gls', 0, 'run_makeglossaries' );
add_cus_dep( 'acn', 'acr', 0, 'run_makeglossaries' );
push @generated_exts, 'glo', 'gls', 'glg';
push @generated_exts, 'acn', 'acr', 'alg';
sub run_makeglossaries {
   my ($base, $ext) = @_;
   system( "makeglossaries \"$base\"" );
}
