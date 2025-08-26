pkgname=wallgui-bin
pkgver=0.0.1
pkgrel=1
pkgdesc="Modern GTK4 wallpaper manager (prebuilt binary)"
arch=('x86_64')
url="https://github.com/jr4dh3y/wallgui"
license=('MIT')
depends=('gtk4' 'python' 'python-gobject' 'swww' 'mpvpaper' 'ffmpeg' 'wallust')
provides=('wallgui')
conflicts=('wallgui')
source=("$url/releases/download/v$pkgver/wallgui-$pkgver-x86_64"
        "wallgui.desktop"
        "LICENSE")
sha256sums=('SKIP'
            'SKIP'
            'SKIP')

package() {
  install -Dm755 "$srcdir/wallgui-$pkgver-x86_64" "$pkgdir/usr/bin/wallgui"
  install -Dm644 "$srcdir/wallgui.desktop" "$pkgdir/usr/share/applications/wallgui.desktop"
  install -Dm644 "$srcdir/LICENSE" "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}
