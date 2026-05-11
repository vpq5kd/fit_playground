import ROOT
import argparse

ROOT.gStyle.SetOptStat(0)

parser = argparse.ArgumentParser('simple script to compare templates')
parser.add_argument('--templates', nargs="+")
parser.add_argument('--labels', nargs="+")
parser.add_argument('--title', type=str)
args = parser.parse_args()


hists = []
for template in args.templates:
    print(template)
    f = ROOT.TFile.Open(template)
    h = f.Get("p").Clone()
    h.SetDirectory(0)
    hists.append(h)

colors = [ROOT.kRed, ROOT.kBlue]

c = ROOT.TCanvas("c", "", 800, 600)
c.SetLeftMargin(0.15)
c.SetBottomMargin(0.12)
c.SetRightMargin(0.05)
c.SetTopMargin(0.08)

for i, hist in enumerate(hists):
    hist.SetLineColor(colors[i % len(colors)])
    hist.SetLineWidth(2)

    if i == 0:
        hist.SetTitle(args.title)
        hist.Draw("HIST")
    else:
        hist.Draw("HIST SAME")

legend = ROOT.TLegend(0.7,0.7,0.9,0.9)
for i, label in enumerate(args.labels):
    legend.AddEntry(hists[i], label, "l")
legend.Draw()

input("Press enter to exit...")
