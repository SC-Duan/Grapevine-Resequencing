#!usr/bin/perl -w
use strict;
use FileHandle;
die "\n Usage perl $0 <fa><snp><length>\n" unless (@ARGV==3);
$/="\>";
open (AF,"$ARGV[0]")||die "$!";
<AF>;
my %hash;
while (<AF>)
{chomp;
 my @aa=split /\n/,$_;
 my $chr=shift @aa;
 $chr=(split /\s+/,$chr)[0];
 #print "$chr\n";
 my $seq=join"",@aa;
 $hash{$chr}=$seq;
}
close AF;

$/="\n";
open (BF,"$ARGV[1]")||die "$!";
#open (OUT,">$ARGV[2]")||die "$!";
my %fh;
<BF>; 
my $le=$ARGV[2];
while (<BF>)
{chomp;
  my @aa=split;
  my $start;
  my $sub1=0;
  my $sub2=0;
  if ($aa[1]<$le+1)
   {$sub1=$aa[1]-1; $start=0;
     $sub2=100;}
  elsif ((length $hash{$aa[0]})-$aa[1]<$le)
    {$sub2=(length $hash{$aa[0]})-$aa[1];
     $sub1=$le;
      $start=$aa[1]-$le-1;}
  else{$sub1=$le;$sub2=$le;$start=$aa[1]-$le-1;}
  
  my $seq1=substr $hash{$aa[0]},$start,$sub1;
  my $mid=substr $hash{$aa[0]},$aa[1]-1,1;
  my $seq2=substr $hash{$aa[0]},$aa[1],$sub2;
  my $alle=(split /,/,$aa[3])[0];
  my $name=$aa[0]."_".$aa[1]."_".$aa[2]."_".$alle;
   $alle="[".$aa[2]."/".$alle."]";
   if (!exists $fh{$aa[0]})
        {$fh{$aa[0]}=FileHandle -> new(">$aa[0].info");} 
  if ($mid ne $aa[2])
      {print "$name error\n";}
    else
        {$fh{$aa[0]} ->print("$name\t$seq1$alle$seq2\n");}
    }
close BF;
foreach (keys %fh)
 {$fh{$_} -> close();}
    
